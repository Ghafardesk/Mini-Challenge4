from bs4 import BeautifulSoup


def clean_html(html: str) -> str:
    if not html:
        return ""

    soup = BeautifulSoup(html, "html.parser")

    for tag in soup.select(
        "script, style, noscript, svg, iframe, nav, header, footer, aside, form, button, select"
    ):
        tag.decompose()

    keep_tags = ["p", "li", "td", "th", "h1", "h2", "h3", "h4", "h5", "h6", "span", "div", "table", "article", "section", "main"]
    fragments: list[str] = []

    for tag in soup.find_all(keep_tags):
        text = tag.get_text(" ", strip=True)
        if text:
            fragments.append(text)

    return "\n".join(fragments)
