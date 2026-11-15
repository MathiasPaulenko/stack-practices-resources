# Jest Snapshot Testing — Proyecto complementario

Companion ejecutable de la receta [Snapshot Testing de Componentes React con Jest](https://stackpractices.com/es/recipes/jest-snapshot-testing/) en StackPractices.

Un setup mínimo de Jest + React Testing Library con cinco componentes que ejercitan cada patrón de la receta, más archivos `.snap` commiteados para que veas cómo luce un snapshot real.

## Archivos

| Ruta | Qué muestra |
|---|---|
| `src/Button.test.jsx` | `toMatchSnapshot()` básico sobre `container.firstChild`, un test por variante |
| `src/Card.test.jsx` | Snapshot por estado significativo (todas las props, sin imagen, cargando) |
| `src/Badge.test.jsx` | `toMatchInlineSnapshot()` — la salida esperada vive dentro del archivo de test |
| `src/UserProfile.test.jsx` | Snapshots con `asFragment()` de Testing Library |
| `src/LastLogin.test.jsx` | `jest.useFakeTimers().setSystemTime()` para timestamps deterministas |
| `src/Dashboard.test.jsx` + `src/lib/__mocks__/Chart.jsx` | Mock manual que reemplaza un componente de terceros por un stub estable |
| `src/__snapshots__/` | Los `.snap` que Jest generó en la primera ejecución — commiteados a propósito |

## Ejecución

```bash
npm install
npm test          # los 11 tests pasan contra los snapshots commiteados
```

Luego prueba el flujo:

```bash
npm run test:ci       # modo CI: snapshots ausentes fallan en vez de escribirse
npm run test:update   # bendice cambios intencionales (igual que jest -u)
npm run test:watch    # pulsa i para revisión interactiva de snapshots
```

## Cosas para probar

1. **Rompe un snapshot**: cambia el `className` en `src/Button.jsx` y corre `npm test`. El diff muestra exactamente qué variante se movió.
2. **Genera un snapshot obsoleto**: renombra un test en `Card.test.jsx` — Jest reporta `1 obsolete snapshot`; `npm run test:update` lo limpia.
3. **Siente el flake**: comenta `jest.mock('./lib/Chart')` en `Dashboard.test.jsx` y corre `npm test` dos veces — el `style.width` aleatorio de `src/lib/Chart.jsx` rompe el snapshot cada vez. Por eso la salida de terceros se reemplaza por stubs.
4. **Regeneración inline**: vacía el template string en `Badge.test.jsx` y corre `npm test -- -u`; Jest lo reescribe (requiere Prettier 2 — ver abajo).

## Notas

- `jest-environment-jsdom` es un paquete separado desde Jest 28.
- `prettier` queda en v2 a propósito: Jest 29 aún no puede escribir snapshots inline contra Prettier 3+.
- `babel.config.js` usa `@babel/preset-react` con `runtime: 'automatic'`, así que no hace falta `import React` en los componentes.
