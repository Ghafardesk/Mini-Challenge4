import argparse
import json
from pathlib import Path

from .agent import run_agent
from .types import QueryRequest


def parse_input_payload(raw_input: str | None) -> dict:
    if raw_input is None:
        return {}

    trimmed = raw_input.strip()
    if not trimmed:
        return {}

    if trimmed.startswith("{"):
        return json.loads(trimmed)

    if Path(trimmed).exists():
        return json.loads(Path(trimmed).read_text(encoding="utf-8"))

    return json.loads(trimmed)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Web retrieval agent for AMD AI League Match 4")
    parser.add_argument("--query", help="Natural-language question")
    parser.add_argument("--url", help="Optional starting URL")
    parser.add_argument("--input-json", help="Input JSON string or path to a JSON file")
    parser.add_argument("--output", help="Path to save the JSON output file")
    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()

    payload = parse_input_payload(args.input_json) if args.input_json else {}
    request = QueryRequest(**{**payload, "query": payload.get("query") or args.query, "url": payload.get("url") or args.url})

    if not request.query:
        parser.error("A query must be provided via --query or JSON input.")

    result = run_agent(request.query, starting_url=request.url)
    output = {
        "answer": result.answer,
        "source_url": result.source_url,
        "confidence": float(result.confidence),
    }

    if args.output:
        Path(args.output).write_text(json.dumps(output), encoding="utf-8")
    else:
        print(json.dumps(output))

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
