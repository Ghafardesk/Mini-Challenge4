import re


def classify_answer_type(query: str) -> str:
    q = (query or "").lower()

    if any(term in q for term in ["price", "cost", "fee", "amount", "pay", "priced"]):
        return "price"
    if any(term in q for term in ["version", "release", "build", "revision"]):
        return "version"
    if any(term in q for term in ["date", "when", "published", "updated", "launched"]):
        return "date"
    if any(term in q for term in ["how many", "count", "total", "number", "quantity"]):
        return "number"
    if re.search(r"\b\d+\b", q):
        return "number"
    return "string"
