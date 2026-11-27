# State Machine UI Pattern

Runnable companion for the [State Machine UI pattern](https://stackpractices.com/patterns/state-machine-ui-pattern/): finite state machines for UI components, from a plain `useReducer` FSM up to XState machines with guards, invoked services, nested states, and actors.

## Contents

- `useFormMachine.js` — dependency-free FSM built on `useReducer`: idle → submitting → success/error
- `ContactForm.jsx` — a form component consuming `useFormMachine`
- `fetchMachine.js` — XState machine for data fetching with `invoke`, `CANCEL`, and a guarded `RETRY` (max 3 attempts)
- `DataFetcher.jsx` — React component driven by `useMachine(fetchMachine)`
- `checkoutMachine.js` — multi-step wizard: cart → shipping → payment → review → processing → confirmation/error
- `Checkout.jsx` — the wizard UI wired to `checkoutMachine`
- `toggleMachine.js` — minimal two-state machine
- `Dropdown.jsx` — dropdown with `open`/`closed` states plus `SELECT`, `CLICK_OUTSIDE`, and `ESCAPE` events
- `authMachine.js` — guarded transitions: `RETRY` allowed only while `loginAttempts < 3`
- `fileUploadMachine.js` — hierarchical states: `uploading` nests `sending`/`failed`/`done`
- `concurrentUploads.js` — actor model: `spawn` one upload machine per file
- `package.json` — React 19 + XState 5

## Notes

- Model states, not flags: `state.matches('loading')` replaces `isLoading && !isError`.
- Events not listed for a state are ignored — that's how impossible transitions are prevented.
- Use `invoke` for async work so the machine tracks it; keep `assign` for synchronous context updates.
- The example components call `/api/...` endpoints — wire them to your backend or a mock (MSW) to run them.
