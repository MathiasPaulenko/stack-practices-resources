# React Server Components — Scaffold de Next.js App Router

Compañero ejecutable de [Guía Completa de React Server Components: Arquitectura RSC](https://stackpractices.com/es/guides/complete-guide-react-server-components/). Una app mínima de Next.js 15 (App Router) que reproduce los patrones de la guía sobre stubs en memoria — no requiere base de datos ni proveedor de auth.

## Qué contiene

| Archivo | Patrón de la guía |
| --- | --- |
| `app/products/page.tsx` | Server Component con carga de datos en paralelo: componentes async hermanos bajo `<Suspense>` separados, más `export const revalidate` (ISR) |
| `lib/queries.ts` | Dedup por request de React `cache()` compartido entre componentes (`generateMetadata` + página hacen una sola consulta) |
| `lib/db.ts` | Stub async tipado que reemplaza a Prisma — firmas con estilo Prisma y latencia simulada para que el streaming se note |
| `lib/auth.ts` | Stub de `auth()` que devuelve una sesión demo — poné `isAdmin` en `false` para ver el camino de `Unauthorized` |
| `lib/serialize.ts` | Mapeo por allowlist a props serializables antes de cruzar la frontera server/client |
| `app/products/ProductCard.tsx` | Server Component async que compone islas client (`LikeButton`, `AddToCartButton`) solo con props serializables |
| `app/products/[id]/page.tsx` | `params` como Promise, fetches independientes en `Promise.all`, fetches dependientes después, `notFound()`, `generateMetadata`, `force-dynamic` para datos del viewer |
| `app/products/actions.ts` | Server actions `"use server"`: `createProduct` (zod + auth + `revalidatePath`), `toggleLike`, `deleteProduct`, `addToCart` |
| `app/products/CreateProductForm.tsx` | Formulario `"use client"` conectado con `useActionState` |
| `app/products/LikeButton.tsx` | UI optimista `"use client"` con `useOptimistic` + `useTransition` |
| `app/products/AddToCartButton.tsx`, `DeleteProductButton.tsx` | Hojas client que llaman Server Actions desde event handlers |
| `app/loading.tsx`, `app/error.tsx`, `app/not-found.tsx`, `app/products/[id]/error.tsx` | Boundaries de loading/error/not-found por segmento — `error.tsx` debe ser Client Component y los boundaries se anidan por segmento |
| `test/` | Tests unitarios con Vitest para la lógica pura: validación zod del form y serialización de props |

## Prerrequisitos

- Node.js 20+
- npm

## Ejecutarlo

```bash
npm install
npm run dev
```

Abrí http://localhost:3000 — `/` muestra una tira de destacados, `/products` el catálogo con secciones en streaming paralelo, `/products/[id]` la página de detalle con fetches dependientes.

## Testear la lógica pura

```bash
npm test
```

Corre `vitest` sobre `test/` — cubre `lib/product-schema.ts` (la validación zod que usa el Server Action) y `lib/serialize.ts` (el mapeo a props seguras para client). No necesita el runtime de Next.js, pero sí `npm install` para `zod` y `vitest`.

## Otros scripts

```bash
npm run typecheck   # tsc --noEmit
npm run lint        # next lint
npm run build       # build de producción
```

## Notas

- `lib/db.ts` es un stub en memoria, no Prisma — reemplazá los cuerpos de los métodos por un cliente real; las firmas ya imitan las de Prisma.
- `auth()` siempre devuelve el admin demo. Poné `isAdmin: false` en `lib/auth.ts`, enviá el formulario y vas a ver el estado `Unauthorized` en lugar de un producto creado.
- El modelo `'use cache'` / `cacheComponents` de la guía quedó intencionalmente desactivado — este scaffold usa los exports clásicos `revalidate` / `dynamic` para que ambas palancas de caching se vean en el código.
