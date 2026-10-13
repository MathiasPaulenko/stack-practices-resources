# Renderizado en el servidor (SSR) — Archivos complementarios

Ejemplos ejecutables de la receta:
<https://stackpractices.com/es/recipes/server-side-rendering/>

## Archivos

| Archivo | Qué muestra |
|---------|-------------|
| `nextjs-page.tsx` | Server component de Next.js App Router: fetch en el servidor, ISR con `revalidate`, streaming con `<Suspense>` |
| `astro-island.astro` | Islas de Astro: HTML sin JS por defecto, hidratación parcial con directivas `client:*` |
| `express-ssr.js` | SSR mínimo a mano con Express + `renderToString` + `hydrateRoot` — lo que abstraen los frameworks |

## Puntos clave

- **SSR** renderiza el HTML por petición en el servidor — primer paint rápido, marcado rastreable.
- **Hidratación** adjunta los event listeners a ese HTML en el cliente — de ahí viene la interactividad.
- Los server components / frontmatter corren solo en el servidor: los secretos y el código de fetch nunca llegan al bundle del navegador.
- Cachea la salida SSR en el edge (`s-maxage` + `stale-while-revalidate`) para absorber la mayoría de peticiones.
- Mantén el output del render determinista (`Date.now()`, `Math.random()`, `window`) o tendrás hydration mismatches.

## Cuándo NO usar SSR

Dashboards autenticados, apps offline-first y páginas estáticas con mucho tráfico — ahí CSR o SSG salen más baratos.
