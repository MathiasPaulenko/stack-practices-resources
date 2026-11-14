# JavaScript Infinite Scroll Pagination — Companion Resources

Companion code for the [JavaScript Infinite Scroll Pagination](https://stackpractices.com/recipes/javascript-infinite-scroll-pagination/) recipe on StackPractices.

## Contents

| File | Description |
| --- | --- |
| `infinite_scroll.js` | `InfiniteScroll` class — IntersectionObserver, loading/error states, `AbortController` teardown, `DocumentFragment` batching, a11y roles |
| `use_infinite_scroll.jsx` | React hook with a synchronous `useRef` guard against double fetches |
| `demo.html` | Runnable demo page wired to the class (ES module, no bundler) |
| `mock_server.js` | Zero-dep `node:http` server: serves the demo + a fake `/api/posts` (120 posts) |
| `mock_server.test.js` | `node:test` tests for the pagination contract |
| `package.json` | ESM config + `npm start` / `npm test` |

## Requirements

- Node.js 18+ (built-in `fetch` for tests)

## Run the demo

```bash
npm start
# open http://127.0.0.1:8010/demo.html and scroll down
```

The mock API returns 12 posts per page, 120 total — `hasMore` flips to `false` on page 10 and the demo shows the end message.

## Run the tests

```bash
npm test
```

Covers the contract the observer relies on: slice math, `hasMore` edges, `page`/`limit` params over real HTTP.

## Notes

- The class and hook are drop-in — point `fetchUrl` at any API that answers `{ items, hasMore }`.
- If your dataset is write-heavy, ask the API for cursor pagination (`?after=<last-id>`) instead of `?page=N`; offsets drift when items prepend.
- For lists over ~1k rendered items, prefer a virtual list (`react-window`) — see the recipe's variants table.
