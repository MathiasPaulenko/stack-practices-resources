# Patrón Suspense Boundary — Ejemplos en React

Ejemplos ejecutables del [patrón Suspense Boundary](https://stackpractices.com/es/patterns/suspense-boundary-pattern/): estados de carga declarativos con boundaries `<Suspense>`, un recurso compatible con suspense y caché de promesas, fallbacks skeleton y un error boundary.

## Archivos

| Archivo | Propósito |
|---------|-----------|
| `App.jsx` | App con boundaries Suspense anidados dentro de un error boundary |
| `suspenseResource.js` | `wrapPromise` + caché mínimos para que `read()` pueda suspender sin riesgo |
| `ErrorBoundary.jsx` | Error boundary de clase con UI de fallback y reintento |
| `Skeletons.jsx` | Fallbacks skeleton con la forma del contenido |
| `package.json` | Dependencias de React 19 |

## Uso

```jsx
import { Suspense } from 'react';
import ErrorBoundary from './ErrorBoundary';
import { UserCardSkeleton } from './Skeletons';

<ErrorBoundary>
  <Suspense fallback={<UserCardSkeleton />}>
    <UserCard userId={42} />
  </Suspense>
</ErrorBoundary>
```

Reglas clave: cachea la promesa (nunca llames a `fetch()` a pelo en el render), haz que el fallback coincida con la forma del contenido y combina siempre Suspense con un error boundary — Suspense solo maneja la carga, no los fallos.
