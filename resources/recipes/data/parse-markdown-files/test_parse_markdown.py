"""Tests for the parse_markdown helpers. Run: pytest test_parse_markdown.py -v"""

from pathlib import Path

from parse_markdown import (
    extract_headings,
    extract_links,
    split_frontmatter,
    to_html,
)

POST = (Path(__file__).parent / "post.md").read_text(encoding="utf-8")


def test_to_html_heading():
    assert "<h1>Hello</h1>" in to_html("# Hello")


def test_to_html_table_needs_extension():
    assert "<table>" in to_html(POST)


def test_split_frontmatter():
    meta, body = split_frontmatter(POST)
    assert "title: My Post" in meta
    assert body.startswith("# Hello")
    assert "---" not in body


def test_no_frontmatter():
    meta, body = split_frontmatter("# Just a doc")
    assert meta == []
    assert body == "# Just a doc"


def test_extract_headings():
    assert extract_headings(POST) == [(1, "Hello"), (2, "A section")]


def test_extract_links():
    assert extract_links(POST) == ["https://example.com"]
