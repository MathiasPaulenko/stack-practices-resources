# Truncate Text

Runnable examples for [stackpractices.com/recipes/truncate-text/](https://stackpractices.com/recipes/truncate-text/).

| File | Shows |
|------|-------|
| `truncate_text.py` | Character slice + word-boundary `textwrap.shorten` |
| `truncate-text.js` | Character slice, word boundary, and `Intl.Segmenter` grapheme-safe cut |
| `TextTruncator.java` | `StringUtils.abbreviate` + word-boundary loop |
| `truncate.css` | Single-line `text-overflow: ellipsis` and multi-line `line-clamp` |

## Run

```bash
python truncate_text.py
node truncate-text.js
javac TextTruncator.java && java TextTruncator
```

For UI text, prefer CSS — the full string stays in the DOM and nothing is destroyed.
