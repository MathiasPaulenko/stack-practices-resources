# Reactive State with Svelte Stores — Examples

Runnable examples for the [Svelte stores recipe](https://stackpractices.com/recipes/svelte-store-reactive-state/): `writable`, `readable`, `derived`, a custom store with a contract-based API, localStorage persistence, and store tests.

## Files

| File | Purpose |
|------|---------|
| `stores/counter.js` | Custom store exposing `increment`/`decrement`/`reset` only |
| `stores/time.js` | `readable` store with start/stop lifecycle per subscriber |
| `stores/cart.js` | `writable` + `derived` chain (count, total, formatted total) |
| `stores/user.js` | Session store persisted to `localStorage` |
| `Counter.svelte` | Component using `$store` auto-subscription |
| `counter.test.js` | Vitest tests using `get()` for one-shot reads |
| `package.json` | Svelte 5 + Vitest |

## Usage

```javascript
import { counter } from "./stores/counter.js";
import { get } from "svelte/store";

counter.increment();
console.log(get(counter)); // 5
```

In components, use the `$` prefix (`{$counter}`) — Svelte handles subscription and cleanup automatically.

Run tests: `npm install && npm test`.
