# Lazy Loading — Companion Resources

Runnable examples for the [Lazy Loading](https://stackpractices.com/recipes/lazy-loading/) recipe on StackPractices.

## Files

| File | Purpose |
|------|---------|
| `index.html` | Offline demo page: one eager hero + 11 IntersectionObserver-driven images |
| `intersection-observer.js` | Shared observer with `rootMargin`, `unobserve`, and `onerror` fallback |
| `make-placeholders.py` | Generates local SVG placeholders so the demo needs no network |
| `LazyComponents.jsx` | `React.lazy` + `Suspense` with skeleton fallbacks and an error boundary |
| `use-infinite-list.jsx` | `useInfiniteQuery` + sentinel observer = infinite scroll |

## Quick start

```bash
# 1. Generate the placeholder images (12 SVGs + a fallback)
python make-placeholders.py

# 2. Open the demo
#    Either double-click index.html, or serve it:
python -m http.server 8080
# then browse http://localhost:8080
```

Open DevTools → Network, throttle to Slow 3G, and scroll slowly. The counter in the corner shows how many images have actually fetched — the ones you never scroll to never download.

## What to try

- Change `rootMargin` in `intersection-observer.js` from `200px` to `0px` and scroll fast — you'll see images pop in late.
- Comment out the `width`/`height` attributes in `index.html` and watch the layout shift (CLS) as images land.
- Break one `data-src` path to see the `onerror` fallback kick in.

## React snippets

`LazyComponents.jsx` shows why every `React.lazy` needs an error boundary: a chunk that 404s (new deploy, stale HTML) throws on render and crashes the tree without one.

`use-infinite-list.jsx` uses cursor pagination (`after=…`) instead of `page=n` — cursors don't drift when rows are inserted between fetches, which is how you avoid duplicate items in feeds.
