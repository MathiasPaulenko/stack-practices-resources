# Pagination — Companion Files

Companion files for [Pagination](https://stackpractices.com/recipes/pagination/) on StackPractices.

## Contents

- `pagination.py` — runnable offset + cursor implementations over a 100-row in-memory dataset. Run it: `python pagination.py`.
- `test_pagination.py` — pytest suite covering first/deep/last pages, the `page_size + 1` probe, empty results past the end, and a full cursor walk. Run it: `pytest test_pagination.py`.

## What to look at

- `get_users_cursor` fetches `page_size + 1` rows — the probe answers `has_more` without a `COUNT(*)`, and `next_cursor` is derived from the last returned item, never the probe.
- `walk_all_pages` is the consumer pattern: pass `next_cursor` back until `has_more` is false. Page 1 and page 10,000 cost the same — that's the whole point over offset.
