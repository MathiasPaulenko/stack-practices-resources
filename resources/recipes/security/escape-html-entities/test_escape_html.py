"""Tests for escape_html.py — run with: pytest test_escape_html.py -v"""

from escape_html import escape_html, safe_json_for_script, safe_url


class TestEscapeHtml:
    def test_escapes_script_payload(self):
        assert escape_html('<script>alert("xss")</script>') == (
            '&lt;script&gt;alert(&quot;xss&quot;)&lt;/script&gt;'
        )

    def test_escapes_all_five_characters(self):
        assert escape_html("<>&\"'") == "&lt;&gt;&amp;&quot;&#x27;"

    def test_escapes_event_handler_injection(self):
        assert escape_html('<img src=x onerror=alert(1)>') == (
            '&lt;img src=x onerror=alert(1)&gt;'
        )

    def test_plain_text_unchanged(self):
        assert escape_html("Hello, world!") == "Hello, world!"


class TestSafeJsonForScript:
    def test_script_breakout_is_neutralized(self):
        out = safe_json_for_script({"name": 'x</script><script>alert(1)</script>'})
        assert "</script>" not in out
        assert "\\u003c" in out

    def test_line_separators_escaped(self):
        out = safe_json_for_script({"text": "a\u2028b\u2029c"})
        assert "\u2028" not in out
        assert "\\u2028" in out
        assert "\\u2029" in out

    def test_output_still_parses_as_json(self):
        import json
        data = {"user": "Alice & Bob", "n": 42}
        out = safe_json_for_script(data)
        # json.loads accepts the  escapes back into real characters
        assert json.loads(out) == data


class TestSafeUrl:
    def test_rejects_javascript_scheme(self):
        assert safe_url("javascript:alert(1)") == ""

    def test_rejects_data_scheme(self):
        assert safe_url("data:text/html,<script>alert(1)</script>") == ""

    def test_accepts_https(self):
        assert safe_url("https://example.com/path?q=1") == (
            "https://example.com/path?q=1"
        )

    def test_accepts_relative_url(self):
        assert safe_url("/docs/getting-started") == "/docs/getting-started"

    def test_accepts_mailto(self):
        assert safe_url("mailto:team@example.com") == "mailto:team@example.com"

    def test_reencodes_spaces(self):
        assert safe_url("https://example.com/a b") == "https://example.com/a%20b"
