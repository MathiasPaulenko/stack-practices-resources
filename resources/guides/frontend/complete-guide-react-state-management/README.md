# React State Management — Vite Playground Scaffold

Runnable companion to [Complete Guide to React State Management: Zustand, Jotai, TanStack Query](https://stackpractices.com/guides/complete-guide-react-state-management/). A minimal Vite + React + TypeScript app that implements the **same domain** — products, cart, theme — four different ways, switchable from a tab bar.

## What's inside

| File | Pattern from the guide |
| --- | --- |
| `src/context/ThemeContext.tsx` | Context API: `createContext` + `useReducer` + memoized `value` via `useMemo` (the fix every Context example skips) |
| `src/context/CartContext.tsx` | Context with `useReducer` for cart transitions; the reducer delegates to pure helpers |
| `src/lib/cart.ts` | Pure cart logic (`upsert`, `setQuantity`, `remove`, `recalcTotal`, `serialize`/`parse`) shared by the Context reducer, the Zustand store, and the Jotai write atoms |
| `src/stores/useThemeStore.ts` | Zustand store — module singleton, no provider, slice selectors |
| `src/stores/useCartStore.ts` | Zustand with `devtools` + `persist` middleware; `partialize`/`merge` rebuild the derived `total` on rehydration |
| `src/atoms/themeAtoms.ts` | Jotai primitive atom + write-only derived atoms (`toggleThemeAtom`) |
| `src/atoms/cartAtoms.ts` | Jotai primitive + derived atoms (`cartTotalAtom`, `cartItemCountAtom`), `atomFamily` for per-item quantity, and write-only "action" atoms |
| `src/query/queryClient.ts` | `QueryClient` defaults: deliberate `staleTime`/`gcTime`, single retry |
| `src/query/productsQuery.ts` | `useQuery` with `staleTime`, `usePaginatedProducts` with `keepPreviousData`, `useCreateProduct` with the snapshot → mutate → settle optimistic pattern and rollback |
| `src/api.ts` | In-memory mock REST API with simulated latency, including a `fail` flag to demo rollback |
| `src/components/` | `ModeTabs` switches approaches; `context/`, `zustand/`, `jotai/` each ship `ThemeToggle` + `CartView` + `AddToCartButton`; `query/` has the server-state playground; `ProductList`/`CartPanel` are shared presentational pieces |
| `src/App.tsx` | Composes providers per mode — the "query" tab reproduces the guide's "Putting It Together" combo (Context theme + Zustand cart + TanStack Query) |
| `test/` | Vitest unit tests for the pure logic: cart helpers, Zustand stores via `getState()`, Jotai atoms via a vanilla `createStore()` — no React runtime needed |

## Prerequisites

- Node.js 20+
- npm

## Run it

```bash
npm install
npm run dev
```

Open http://localhost:5173 — the tab bar switches between Context API, Zustand, Jotai, and the TanStack Query combo. Add products to the cart, toggle the theme, and compare how each approach behaves. The Zustand cart persists to `localStorage`, so it survives reloads.

## Test the pure logic

```bash
npm test
```

Runs `vitest` over `test/` — covers `lib/cart.ts` (upsert/quantity/total/serialization), the Zustand stores (`getState()`/`setState()` without React), and the Jotai atoms (vanilla `createStore`).

## Other scripts

```bash
npm run typecheck   # tsc --noEmit
npm run build       # production build
npm run preview     # serve the production build
```

## Notes

- **Products are always server state.** Every tab loads them through TanStack Query — that's the guide's core split. The tabs compare *client* state (theme + cart); only the "TanStack Query" tab adds the pagination and optimistic-mutation playground.
- **Each mode owns independent state.** Switching tabs doesn't migrate the cart or theme — except the Zustand cart, which persists via `localStorage`.
- **Immer was swapped for pure helpers.** The guide's Zustand example uses `immer`; this scaffold routes every mutation through `lib/cart.ts` instead, so the same transitions are unit-tested and shared verbatim with the Context reducer and Jotai atoms.
- **`persist` got a storage fallback.** `localStorage` doesn't exist in Node, so the store falls back to an in-memory map there — the tests exercise the real store without a DOM.
- **`atomFamily` comes from `jotai/utils`.** The guide imports it from `"jotai"` for brevity; in Jotai v2 it's a util export (and in v3 it moved to the `jotai-family` package).
