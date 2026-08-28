"""URL encoding and decoding examples in Python."""
from urllib.parse import quote, unquote, urlencode, parse_qs, urlparse


def encode_value(value: str) -> str:
    """Encode a string for a path or query value."""
    return quote(value)


def build_query_string(params: dict) -> str:
    """Build a query string safely from a dict."""
    return urlencode(params)


def parse_url(url: str) -> dict:
    """Parse a URL and return its query parameters as a dict."""
    parsed = urlparse(url)
    return parse_qs(parsed.query)


def decode_value(encoded: str) -> str:
    """Decode a percent-encoded string."""
    return unquote(encoded)


if __name__ == "__main__":
    # Encode
    encoded = encode_value("hello world & friends")
    print(f"Encoded: {encoded}")  # hello%20world%20%26%20friends

    # Build query string
    query = build_query_string({"search": "python & java", "page": 2})
    print(f"Query: {query}")  # search=python+%26+java&page=2

    # Parse URL
    params = parse_url("https://api.example.com/search?query=hello%20world&limit=10")
    print(f"Parsed: {params}")  # {'query': ['hello world'], 'limit': ['10']}

    # Decode
    decoded = decode_value("hello%20world")
    print(f"Decoded: {decoded}")  # hello world
