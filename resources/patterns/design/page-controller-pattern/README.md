# Page Controller Pattern — Companion Files

Companion files for [Page Controller Pattern](https://stackpractices.com/patterns/page-controller-pattern/) on StackPractices.

## Contents

- `page_controller.py` — runnable example: `Request`/`Response`, three page controllers, and the flat path→controller map. Run it: `python page_controller.py`.
- `test_page_controller.py` — pytest suite covering routing, parameter handling, a 404, and page-specific logic. Run it: `pytest test_page_controller.py`.

## What to look at

- Each controller owns one page end to end — nothing shared between them.
- `CONTROLLERS` is the whole routing story: adding a page is one class + one entry. When the map needs patterns, middleware, or shared preprocessing, that's the Front Controller threshold.
- `test_route_map_stays_declarative` guards the map itself — a common silent-404 source.
