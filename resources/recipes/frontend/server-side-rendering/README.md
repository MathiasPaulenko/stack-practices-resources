# Server-Side Rendering — Companion Files

Runnable examples for the recipe:
<https://stackpractices.com/recipes/server-side-rendering/>

## Files

| File | What it shows |
|------|---------------|
| `nextjs-page.tsx` | Next.js App Router server component: server-side fetch, ISR with `revalidate`, streaming with `<Suspense>` |
| `astro-island.astro` | Astro islands: zero-JS HTML by default, partial hydration via `client:*` directives |
| `express-ssr.js` | Minimal hand-rolled SSR with Express + `renderToString` + `hydrateRoot` — what frameworks abstract away |

## Key takeaways

- **SSR** renders HTML per request on the server — fast first paint, crawlable markup.
- **Hydration** attaches event listeners to that HTML on the client — this is where interactivity comes from.
- Server components / frontmatter run only on the server: secrets and data-fetching code never reach the browser bundle.
- Cache SSR output at the edge (`s-maxage` + `stale-while-revalidate`) to absorb most requests.
- Keep render output deterministic (`Date.now()`, `Math.random()`, `window`) or you get hydration mismatches.

## When NOT to use SSR

Authenticated dashboards, offline-first apps, and high-traffic static pages — CSR or SSG are cheaper there.
