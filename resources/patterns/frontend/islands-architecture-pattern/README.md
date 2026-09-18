# Islands Architecture Pattern — Companion Code

Runnable examples from the
[Islands Architecture pattern](https://stackpractices.com/patterns/islands-architecture-pattern/)
on StackPractices — server-rendered pages that hydrate only their
interactive islands.

## Files

| File | Description |
|------|-------------|
| `islands/page.astro` | Astro page that keeps the product grid static and hydrates only `SearchBox` (client:load) and `NewsletterForm` (client:idle) |
| `islands/SearchBox.jsx` | React island with debounced fetch — the only component shipping React to the browser |
| `islands/CartCounter.jsx` | Second island reading the shared store via `useSyncExternalStore` |
| `islands/NewsletterForm.jsx` | Non-critical island that still works as a plain HTML form before hydration |
| `islands/nanostores-cart.js` | Shared cart store using the real `nanostores` `map()` API — the canonical cross-framework approach |
| `islands/store.js` | Dependency-free shared store with a nanostores-shaped API |
| `islands/vanilla-island.html` | Zero-framework demo: an IntersectionObserver "hydrates" a counter when it scrolls into view — the `client:visible` idea in ~30 lines |
| `islands/hydration-cost.js` | Node script estimating the JS difference between full hydration and islands |

## Usage

The `.astro` / `.jsx` files drop into an Astro project with the React
integration (`npx astro add react`). The vanilla demo needs no build:

```bash
open islands/vanilla-island.html   # or just double-click it
node islands/hydration-cost.js
```

## How It Works

1. The server renders the whole page — including islands — to static HTML.
2. Island props are serialized into the markup as JSON.
3. A tiny runtime hydrates each island when its directive says so
   (`client:load`, `client:visible`, `client:idle`, `client:media`).

Related patterns:
[Progressive Enhancement](https://stackpractices.com/patterns/progressive-enhancement-pattern/) ·
[Suspense Boundary](https://stackpractices.com/patterns/suspense-boundary-pattern/)
