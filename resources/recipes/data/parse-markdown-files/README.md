# Parse Markdown Files — Companion Files

Companion files for [Parse Markdown Files](https://stackpractices.com/recipes/parse-markdown-files/) on StackPractices.

## Contents

- `parse_markdown.py` — `to_html` with explicit extensions, `split_frontmatter`, `extract_headings` and `extract_links`.
- `post.md` — sample post with YAML frontmatter, headings, a table and a link.
- `test_parse_markdown.py` — pytest suite. Run: `pytest test_parse_markdown.py -v` (requires `pip install markdown`).

## What to look at

- `split_frontmatter` first, then parse — feeding `---` to the parser produces a stray heading.
- `test_to_html_table_needs_extension` shows tables are an opt-in extension, not core Markdown.
