# Estado Reactivo con Svelte Stores — Ejemplos

Ejemplos ejecutables de la [receta de stores de Svelte](https://stackpractices.com/es/recipes/svelte-store-reactive-state/): `writable`, `readable`, `derived`, un store personalizado con API por contrato, persistencia en `localStorage` y tests de stores.

## Archivos

| Archivo | Propósito |
|---------|-----------|
| `stores/counter.js` | Store personalizado que solo expone `increment`/`decrement`/`reset` |
| `stores/time.js` | Store `readable` con ciclo de vida start/stop por suscriptor |
| `stores/cart.js` | Cadena `writable` + `derived` (cantidad, total, total formateado) |
| `stores/user.js` | Store de sesión persistido en `localStorage` |
| `Counter.svelte` | Componente usando auto-suscripción `$store` |
| `counter.test.js` | Tests con Vitest usando `get()` para lecturas puntuales |
| `package.json` | Svelte 5 + Vitest |

## Uso

```javascript
import { counter } from "./stores/counter.js";
import { get } from "svelte/store";

counter.increment();
console.log(get(counter)); // 5
```

En los componentes usa el prefijo `$` (`{$counter}`) — Svelte gestiona la suscripción y la limpieza automáticamente.

Ejecutar tests: `npm install && npm test`.
