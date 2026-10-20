from app.agent import run_agent_from_html
from app.verify import verify_answer


def test_verify_answer_detects_literal_match():
    page = "The price is $49.99 today."
    assert verify_answer("$49.99", page) is True
    assert verify_answer("$49.98", page) is False


def test_run_agent_from_html_returns_verified_value():
    html = """
    <html>
      <body>
        <nav>Home About</nav>
        <main>
          <h1>Product</h1>
          <p>Price: $49.99</p>
        </main>
        <footer>Footer</footer>
      </body>
    </html>
    """

    result = run_agent_from_html("What is the price?", html, source_url="https://example.com/product")

    assert result.answer == "$49.99"
    assert result.source_url == "https://example.com/product"
    assert result.confidence > 0.0


def test_run_agent_from_html_rejects_unverifiable_price_query():
    html = """
    <html>
      <body>
        <p>This domain is for use in documentation examples without needing permission.</p>
      </body>
    </html>
    """

    result = run_agent_from_html("What is the price?", html, source_url="https://example.com")

    assert result.answer == ""
    assert result.source_url == ""
    assert result.confidence == 0.0
