import asyncio
import os
import re

from .intent import classify_answer_type
from .types import ExtractionResult

try:
    from pydantic_ai import Agent
    from pydantic_ai.models.openai import OpenAIChatModel
    from pydantic_ai.providers.openai import OpenAIProvider
except ImportError:  # pragma: no cover - dependency installed in Docker image
    Agent = None
    OpenAIChatModel = None
    OpenAIProvider = None


def heuristic_extract(query: str, page_text: str, answer_type: str) -> ExtractionResult:
    text = page_text.strip()
    if not text:
        return ExtractionResult()

    lower_query = (query or "").lower()

    if answer_type == "price":
        matches = re.findall(r"\$\s?\d[\d,]*\.?\d*", text)
        if matches:
            return ExtractionResult(answer=matches[0].replace(" ", ""), confidence=0.8)
        matches = re.findall(r"\b\d+[.,]\d{2}\b", text)
        if matches:
            return ExtractionResult(answer=matches[0], confidence=0.7)

    if answer_type == "version":
        matches = re.findall(r"\bv?\d+\.\d+(?:\.\d+)?(?:[A-Za-z0-9._-]+)?\b", text)
        if matches:
            return ExtractionResult(answer=matches[0], confidence=0.8)

    if answer_type == "date":
        matches = re.findall(r"\b\d{4}-\d{2}-\d{2}\b|\b(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-zA-Z]*\s+\d{1,2},\s+\d{4}\b", text)
        if matches:
            return ExtractionResult(answer=matches[0], confidence=0.8)

    if answer_type == "number":
        matches = re.findall(r"\b\d[\d,]*\.?\d*\b", text)
        if matches:
            return ExtractionResult(answer=matches[0], confidence=0.75)
        return ExtractionResult(answer="", confidence=0.0)

    if answer_type in {"price", "date", "version"}:
        return ExtractionResult(answer="", confidence=0.0)

    if lower_query:
        query_tokens = [token for token in lower_query.split() if token not in {"what", "is", "the", "a", "an", "of", "who", "when", "where", "which", "how"}]
        if not query_tokens:
            return ExtractionResult(answer="", confidence=0.0)

        for sentence in re.split(r"(?<=[.!?])\s+|\n+", text):
            sentence_lc = sentence.lower()
            if any(token in sentence_lc for token in query_tokens[:3]):
                if len(sentence.split()) <= 20:
                    return ExtractionResult(answer=sentence.strip(), confidence=0.65)

    return ExtractionResult(answer="", confidence=0.0)


async def llm_extract(query: str, page_text: str, answer_type: str) -> ExtractionResult:
    if Agent is None:
        return ExtractionResult()

    try:
        model_name = os.getenv("QWEN_MODEL", "qwen3:4b")
        base_url = os.getenv("LOCAL_LLM_BASE_URL", "http://127.0.0.1:11434/v1")
        api_key = os.getenv("LOCAL_LLM_API_KEY", "local-key")

        model = OpenAIChatModel(
            model_name,
            provider=OpenAIProvider(base_url=base_url, api_key=api_key),
        )
        agent = Agent(
            model,
            result_type=ExtractionResult,
            system_prompt=(
                "You are a grounded extraction agent. Return only the exact answer string as it appears in the page. "
                "If the answer is not clearly verifiable in the provided text, return an empty string and confidence 0.0. "
                "Do not infer beyond the actual text."
            ),
        )
        response = await agent.run(
            f"Question: {query}\nAnswer type: {answer_type}\nPage text:\n{page_text[:12000]}"
        )
        return response.data
    except Exception:
        return ExtractionResult()


def select_best_answer(query: str, page_text: str, answer_type: str | None = None) -> ExtractionResult:
    answer_type = answer_type or classify_answer_type(query)

    llm_result = asyncio.run(llm_extract(query, page_text, answer_type))
    if llm_result.answer:
        return llm_result

    heuristic = heuristic_extract(query, page_text, answer_type)
    return heuristic
