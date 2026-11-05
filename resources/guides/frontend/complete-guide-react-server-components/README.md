# React Server Components — Next.js App Router Scaffold

Runnable companion to [Complete Guide to React Server Components: RSC Architecture](https://stackpractices.com/guides/complete-guide-react-server-components/). A minimal Next.js 15 (App Router) app that reproduces the guide's patterns against in-memory stubs — no database or auth provider required.

## What's inside

| File | Pattern from the guide |
| --- | --- |
| `app/products/page.tsx` | Server Component with parallel data loading: sibling async components under separate `<Suspense>` boundaries, plus `export const revalidate` (ISR) |
| `lib/queries.ts` | React `cache()` request-level dedup shared across components (`generateMetadata` + page hit the DB once) |
| `lib/db.ts` | Typed async stub standing in for Prisma — Prisma-flavored signatures, simulated latency so streaming is visible |
| `lib/auth.ts` | `auth()` stub returning a demo session — flip `isAdmin` to `false` and see the `Unauthorized` path |
| `lib/serialize.ts` | Allowlist mapping to serializable props before crossing the server/client boundary |
| `app/products/ProductCard.tsx` | Async Server Component composing client islands (`LikeButton`, `AddToCartButton`) with serializable props only |
| `app/products/[id]/page.tsx` | `params` as a Promise, independent fetches in `Promise.all`, dependent fetches after, `notFound()`, `generateMetadata`, `force-dynamic` for viewer-specific data |
| `app/products/actions.ts` | `"use server"` actions: `createProduct` (zod + auth + `revalidatePath`), `toggleLike`, `deleteProduct`, `addToCart` |
| `app/products/CreateProductForm.tsx` | `"use client"` form wired with `useActionState` |
| `app/products/LikeButton.tsx` | `"use client"` optimistic UI with `useOptimistic` + `useTransition` |
| `app/products/AddToCartButton.tsx`, `DeleteProductButton.tsx` | Client leaves calling Server Actions from event handlers |
| `app/loading.tsx`, `app/error.tsx`, `app/not-found.tsx`, `app/products/[id]/error.tsx` | Segment loading/error/not-found boundaries — `error.tsx` must be a Client Component, and boundaries nest per segment |
| `test/` | Vitest unit tests for the pure logic: zod form validation and client-prop serialization |

## Prerequisites

- Node.js 20+
- npm

## Run it

```bash
npm install
npm run dev
```

Open http://localhost:3000 — `/` shows a featured strip, `/products` the catalog with parallel streaming sections, `/products/[id]` the detail page with dependent fetches.

## Test the pure logic

```bash
npm test
```

Runs `vitest` against `test/` — covers `lib/product-schema.ts` (the zod validation the Server Action uses) and `lib/serialize.ts` (the client-safe prop mapping). No Next.js runtime needed, but `npm install` is still required for `zod` and `vitest`.

## Other scripts

```bash
npm run typecheck   # tsc --noEmit
npm run lint        # next lint
npm run build       # production build
```

## Notes

- `lib/db.ts` is an in-memory stub, not Prisma — swap the method bodies for a real client; the call signatures already mirror Prisma's.
- `auth()` always returns the demo admin. Set `isAdmin: false` in `lib/auth.ts`, submit the form, and you'll get the `Unauthorized` state instead of a created product.
- The `'use cache'` / `cacheComponents` model from the guide is intentionally not enabled — this scaffold sticks to the classic `revalidate` / `dynamic` exports so both caching levers are visible in the code.
