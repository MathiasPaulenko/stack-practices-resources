# URL Encoding — Companion Resources

Runnable examples for the [URL Encoding](https://stackpractices.com/recipes/url-encoding/) recipe.

## Files

| File | Language | Description |
| ------ | -------- | ----------- |
| `url_encoding.py` | Python | Encode, decode, build query strings, parse URLs with urllib |
| `url_encoding.js` | JavaScript | Encode, decode, build query strings, parse URLs with URLSearchParams |
| `UrlEncoding.java` | Java | Encode, decode, build query strings, parse URIs with URLEncoder |

## Quick Start

### Python

```bash
python url_encoding.py
```

### JavaScript

```bash
node url_encoding.js
```

### Java

```bash
javac UrlEncoding.java && java UrlEncoding
```

## Key Points

- Always encode user input before placing it in a URL.
- Use `encodeURIComponent` (JS), `quote` (Python), or `URLEncoder` (Java) for values.
- Use `%20` for paths and `+` for legacy query strings.
- Avoid double-encoding: decode before re-encoding if a value may already be encoded.
- Prefer `URLSearchParams` (JS) and `urlencode` (Python) for query construction.
