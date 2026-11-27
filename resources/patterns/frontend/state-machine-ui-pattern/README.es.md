# Patrón State Machine para UI

Companion ejecutable del [patrón State Machine para UI](https://stackpractices.com/es/patterns/state-machine-ui-pattern/): máquinas de estados finitos para componentes de UI, desde una FSM con `useReducer` hasta máquinas XState con guardas, servicios invocados, estados anidados y actores.

## Contenido

- `useFormMachine.js` — FSM sin dependencias sobre `useReducer`: idle → submitting → success/error
- `ContactForm.jsx` — componente de formulario que consume `useFormMachine`
- `fetchMachine.js` — máquina XState para data fetching con `invoke`, `CANCEL` y un `RETRY` con guarda (máximo 3 intentos)
- `DataFetcher.jsx` — componente React controlado por `useMachine(fetchMachine)`
- `checkoutMachine.js` — wizard multi-paso: cart → shipping → payment → review → processing → confirmation/error
- `Checkout.jsx` — la UI del wizard conectada a `checkoutMachine`
- `toggleMachine.js` — máquina mínima de dos estados
- `Dropdown.jsx` — dropdown con estados `open`/`closed` y eventos `SELECT`, `CLICK_OUTSIDE` y `ESCAPE`
- `authMachine.js` — transiciones con guarda: `RETRY` solo permitido mientras `loginAttempts < 3`
- `fileUploadMachine.js` — estados jerárquicos: `uploading` anida `sending`/`failed`/`done`
- `concurrentUploads.js` — modelo de actores: `spawn` crea una máquina de subida por archivo
- `package.json` — React 19 + XState 5

## Notas

- Modela estados, no flags: `state.matches('loading')` reemplaza a `isLoading && !isError`.
- Los eventos no listados para un estado se ignoran — así se evitan las transiciones imposibles.
- Usa `invoke` para trabajo asíncrono para que la máquina lo rastree; reserva `assign` para actualizaciones síncronas del contexto.
- Los componentes de ejemplo llaman a endpoints `/api/...` — conéctalos a tu backend o a un mock (MSW) para ejecutarlos.
