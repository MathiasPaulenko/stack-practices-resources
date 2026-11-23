"""Markdown parsing helpers matching the recipe's patterns.

Run: pytest test_parse_markdown.py -v
"""

import markdown


def to_html(text, extensions=None):
    """Convert a Markdown string to HTML.

    Enable extensions explicitly — tables and fenced_code are
    GFM-era extensions, not core CommonMark.
    """
    exts = extensions or ["fenced_code", "tables"]
    return markdown.Markdown(extensions=exts).convert(text)


def extract_headings(text):
    """Return [(level, text)] for every ATX heading in the document."""
    headings = []
    for line in text.splitlines():
        stripped = line.lstrip("#")
        if line.startswith("#") and stripped != line:
            headings.append((len(line) - len(stripped), stripped.strip()))
    return headings


def split_frontmatter(text):
    """Split Jekyll-style --- YAML frontmatter from the body.

    Returns (meta_lines, body). Feeding frontmatter to the Markdown
    parser renders the closing --- as a heading, so strip it first.
    """
    lines = text.splitlines()
    if lines and lines[0].strip() == "---":
        for i in range(1, len(lines)):
            if lines[i].strip() == "---":
                return lines[1:i], "\n".join(lines[i + 1 :]).strip()
    return [], text


def extract_links(text):
    """Naive link extractor for inline [text](url) links."""
    import re

    return re.findall(r"\[[^\]]*\]\((https?://[^)\s]+)\)", text)
