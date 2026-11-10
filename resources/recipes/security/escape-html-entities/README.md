# Escape HTML Entities — Companion Resources

Runnable escaping helpers for the three output contexts where HTML escaping alone isn't enough — `<script>`-embedded JSON and URL attributes — plus the classic body/attribute context, in Python, JavaScript, and Java.

Companion to: https://stackpractices.com/recipes/escape-html-entities/

## Files

| File | Language | What it covers |
|------|----------|----------------|
| `escape_html.py` | Python | `html.escape`, JSON-for-`<script>` serializer, `javascript:`-rejecting URL validator |
| `test_escape_html.py` | Python | pytest suite for all three helpers |
| `escapeHtml.js` | JavaScript | Manual entity map, DOM-based escape, `safeJsonInScript`, `safeUrl` |
| `escapeHtml.test.js` | JavaScript | `node:test` suite, zero dependencies |
| `HtmlEscaper.java` | Java | Apache Commons Text + OWASP Encoder per-context variants |

## Run the tests

```bash
# Python (stdlib only, pytest for the suite)
python escape_html.py
pytest test_escape_html.py -v

# JavaScript (Node 18+, built-in test runner)
node --test escapeHtml.test.js
```

`HtmlEscaper.java` requires `commons-text` and `owasp-encoder` on the classpath; it's a reference implementation, not a standalone build.

## What to take away

- Escaping is **context-specific**: body, attribute, `<script>`, URL, and CSS each need their own encoding.
- HTML entities **cannot protect a `<script>` block** — escape `<` as `\u003c` inside embedded JSON instead.
- `javascript:` URLs contain nothing escapable; validate the **scheme**, not the characters.
- Escape at render time, keep the database raw.
