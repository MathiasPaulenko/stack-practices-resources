# React State Management — Scaffold de playground con Vite

Compañero ejecutable de [Guía Completa de React State Management: Zustand, Jotai, TanStack Query](https://stackpractices.com/es/guides/complete-guide-react-state-management/). Una app mínima de Vite + React + TypeScript que implementa el **mismo dominio** — productos, carrito, tema — de cuatro formas distintas, conmutables desde una barra de pestañas.

## Qué contiene

| Archivo | Patrón de la guía |
| --- | --- |
| `src/context/ThemeContext.tsx` | Context API: `createContext` + `useReducer` + `value` memoizado con `useMemo` (el fix que todo ejemplo de Context saltea) |
| `src/context/CartContext.tsx` | Context con `useReducer` para las transiciones del carrito; el reducer delega en helpers puros |
| `src/lib/cart.ts` | Lógica pura del carrito (`upsert`, `setQuantity`, `remove`, `recalcTotal`, `serialize`/`parse`) compartida por el reducer de Context, el store de Zustand y los write atoms de Jotai |
| `src/stores/useThemeStore.ts` | Store de Zustand — singleton a nivel módulo, sin provider, selectores por slice |
| `src/stores/useCartStore.ts` | Zustand con middleware `devtools` + `persist`; `partialize`/`merge` reconstruyen el `total` derivado al rehidratar |
| `src/atoms/themeAtoms.ts` | Atom primitivo de Jotai + atoms derivados de solo escritura (`toggleThemeAtom`) |
| `src/atoms/cartAtoms.ts` | Atom primitivo + atoms derivados (`cartTotalAtom`, `cartItemCountAtom`), `atomFamily` para cantidad por item, y atoms de "acción" de solo escritura |
| `src/query/queryClient.ts` | Defaults del `QueryClient`: `staleTime`/`gcTime` deliberados, un solo retry |
| `src/query/productsQuery.ts` | `useQuery` con `staleTime`, `usePaginatedProducts` con `keepPreviousData`, `useCreateProduct` con el patrón optimista snapshot → mutate → settle y rollback |
| `src/api.ts` | Mock de API REST en memoria con latencia simulada, incluyendo un flag `fail` para demo del rollback |
| `src/components/` | `ModeTabs` cambia de enfoque; `context/`, `zustand/`, `jotai/` traen cada uno `ThemeToggle` + `CartView` + `AddToCartButton`; `query/` tiene el playground de server state; `ProductList`/`CartPanel` son piezas presentacionales compartidas |
| `src/App.tsx` | Compone los providers por modo — la pestaña "query" reproduce el combo de "Putting It Together" de la guía (tema con Context + carrito con Zustand + TanStack Query) |
| `test/` | Tests unitarios con Vitest para la lógica pura: helpers del carrito, stores de Zustand vía `getState()`, atoms de Jotai con `createStore()` vanilla — sin runtime de React |

## Prerrequisitos

- Node.js 20+
- npm

## Ejecutarlo

```bash
npm install
npm run dev
```

Abrí http://localhost:5173 — la barra de pestañas cambia entre Context API, Zustand, Jotai y el combo de TanStack Query. Agregá productos al carrito, cambiá el tema y compará cómo se comporta cada enfoque. El carrito de Zustand persiste en `localStorage`, así que sobrevive recargas.

## Testear la lógica pura

```bash
npm test
```

Corre `vitest` sobre `test/` — cubre `lib/cart.ts` (upsert/cantidad/total/serialización), los stores de Zustand (`getState()`/`setState()` sin React) y los atoms de Jotai (vanilla `createStore`).

## Otros scripts

```bash
npm run typecheck   # tsc --noEmit
npm run build       # build de producción
npm run preview     # sirve el build de producción
```

## Notas

- **Los productos siempre son server state.** Todas las pestañas los cargan vía TanStack Query — esa es la división central de la guía. Las pestañas comparan el *client* state (tema + carrito); solo la pestaña "TanStack Query" suma el playground de paginación y mutación optimista.
- **Cada modo tiene estado independiente.** Cambiar de pestaña no migra el carrito ni el tema — salvo el carrito de Zustand, que persiste vía `localStorage`.
- **Immer se reemplazó por helpers puros.** El ejemplo de Zustand de la guía usa `immer`; este scaffold enruta cada mutación por `lib/cart.ts`, así la misma lógica se testea unitariamente y se comparte textual con el reducer de Context y los atoms de Jotai.
- **`persist` ganó un fallback de storage.** `localStorage` no existe en Node, así que el store cae a un mapa en memoria ahí — los tests ejercitan el store real sin DOM.
- **`atomFamily` viene de `jotai/utils`.** La guía lo importa desde `"jotai"` por brevedad; en Jotai v2 es un export de utils (y en v3 se movió al paquete `jotai-family`).
