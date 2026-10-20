# AMD AI League Match 4: Web Information Retrieval Agent

A containerized retrieval agent that accepts a natural-language query plus an optional starting URL, crawls candidate web pages, cleanly extracts the answer and verifies it exists in the page source before returning JSON.

## Features

- CLI-based query intake via flags or JSON payloads
- Keyless search fallback via DuckDuckGo HTML and direct URL fetch
- DOM cleaning to remove navigation, scripts, and footer noise
- Pydantic AI integration with a local ROCm-backed model endpoint
- Strict answer validation to reject hallucinated values
- Docker packaging using the required ROCm PyTorch base image

## Quick start

```bash
python -m app.cli --query "What is the price?" --url "https://example.com"
```

Or with JSON:

```bash
python -m app.cli --input-json '{"query": "What is the version?", "url": "https://example.com"}'
```

## Output

```json
{"answer": "49.99", "source_url": "https://example.com/product", "confidence": 0.95}
```

If no answer is verifiably present in the page, the agent returns:

```json
{"answer": "", "source_url": "", "confidence": 0.0}
```

## Container build

```bash
docker build -t amd-ai-league-agent .
```

The image is designed for a local ROCm model daemon such as Ollama or a vLLM-style OpenAI-compatible endpoint on the host. The application reads `LOCAL_LLM_BASE_URL` and `QWEN_MODEL` for the endpoint and model selection.
