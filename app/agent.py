from __future__ import annotations

from .dom_clean import clean_html
from .extract import select_best_answer
from .intent import classify_answer_type
from .search import candidate_urls, fetch_html
from .types import AnswerResponse
from .verify import verify_answer


def run_agent_from_html(query: str, html: str, source_url: str = "https://example.com") -> AnswerResponse:
    if not query or not html:
        return AnswerResponse()

    cleaned = clean_html(html)
    if not cleaned:
        return AnswerResponse()

    answer_type = classify_answer_type(query)
    result = select_best_answer(query, cleaned, answer_type)

    if result.answer and verify_answer(result.answer, cleaned):
        return AnswerResponse(answer=result.answer, source_url=source_url, confidence=max(0.0, min(0.99, result.confidence)))

    return AnswerResponse()


def run_agent(query: str, starting_url: str | None = None, max_results: int = 5) -> AnswerResponse:
    if not query:
        return AnswerResponse()

    urls = candidate_urls(query, starting_url=starting_url, max_results=max_results)
    seen: set[str] = set()

    for url in urls:
        if not url or url in seen:
            continue
        seen.add(url)

        try:
            html = fetch_html(url)
        except Exception:
            continue

        if not html:
            continue

        answer = run_agent_from_html(query, html, source_url=url)
        if answer.answer:
            return answer

    return AnswerResponse()
