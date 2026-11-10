"""Context-aware HTML escaping helpers (Python, stdlib only).

Companion to https://stackpractices.com/recipes/escape-html-entities/
Covers three output contexts: HTML body, <script>-embedded JSON, and URLs.
"""

import html
import json
from urllib.parse import quote, urlparse

ALLOWED_URL_SCHEMES = ("http", "https", "mailto", "tel", "")


def escape_html(text: str) -> str:
    """Escape text for an HTML body or double-quoted attribute context.

    Converts < > & " ' into entity references. quote=True (the default
    since Python 3.2) is what makes quotes safe inside attributes.
    """
    return html.escape(text)


def safe_json_for_script(data) -> str:
    """Serialize JSON so it is safe to embed inside a <script> tag.

    HTML entities cannot protect a script block — the parser only looks
    for the literal string </script>. Escaping < and > as unicode
    escapes inside the JSON prevents the payload from forming script
    or comment markup,
    and U+2028/U+2029 are escaped because they are legal in JSON but not
    in JavaScript string literals.
    """
    json_str = json.dumps(data)
    json_str = json_str.replace("<", "\\u003c")
    json_str = json_str.replace(">", "\\u003e")
    json_str = json_str.replace("\u2028", "\\u2028")  # line separator
    json_str = json_str.replace("\u2029", "\\u2029")  # paragraph separator
    return json_str


def safe_url(url: str) -> str:
    """Validate a URL for use in an href/src attribute.

    The attack here is the scheme, not the characters: 'javascript:alert(1)'
    contains nothing HTML-escapable yet still executes on click. Returns
    '' for disallowed schemes, otherwise the URL re-encoded for safe output.
    """
    parsed = urlparse(url)
    if parsed.scheme not in ALLOWED_URL_SCHEMES:
        return ""
    return quote(url, safe=":/?&=%#@")


if __name__ == "__main__":
    payload = '<script>alert("xss")</script>'
    print(escape_html(payload))
    # -> &lt;script&gt;alert(&quot;xss&quot;)&lt;/script&gt;

    print(safe_json_for_script({"name": 'x</script><script>alert(1)</script>'}))
    # -> {"name": "x\\u003c/script>...\\u003c/script>"}

    print(safe_url("javascript:alert(1)"))          # -> ''
    print(safe_url("https://example.com/?q=a b"))   # -> https://example.com/?q=a%20b
