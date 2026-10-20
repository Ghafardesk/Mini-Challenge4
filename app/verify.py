import re


def normalize_space(value: str) -> str:
    return re.sub(r"\s+", " ", value or "").strip()


def verify_answer(answer: str, page_text: str) -> bool:
    if not answer or not page_text:
        return False

    candidate = normalize_space(answer)
    cleaned_page = normalize_space(page_text)
    return candidate in cleaned_page
