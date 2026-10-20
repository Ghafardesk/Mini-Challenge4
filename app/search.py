from __future__ import annotations

from urllib.parse import quote, urljoin

import requests
from bs4 import BeautifulSoup

USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36"


def fetch_html(url: str) -> str:
    if not url:
        return ""

    response = requests.get(url, headers={"User-Agent": USER_AGENT}, timeout=20)
    response.raise_for_status()
    return response.text


def search_duckduckgo(query: str, max_results: int = 5) -> list[str]:
    if not query:
        return []

    encoded = quote(query)
    html = fetch_html(f"https://html.duckduckgo.com/html/?q={encoded}")
    soup = BeautifulSoup(html, "html.parser")
    results: list[str] = []

    for link in soup.select("a.result-link")[:max_results]:
        href = link.get("href")
        if href:
            results.append(urljoin("https://duckduckgo.com/", href))

    return results


def candidate_urls(query: str, starting_url: str | None = None, max_results: int = 5) -> list[str]:
    urls: list[str] = []

    if starting_url:
        urls.append(starting_url)

    for url in search_duckduckgo(query, max_results=max_results):
        if url not in urls:
            urls.append(url)

    return urls
