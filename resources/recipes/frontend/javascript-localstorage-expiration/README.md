# JavaScript LocalStorage with TTL Expiration

Runnable companion code for the [StackPractices recipe](https://stackpractices.com/recipes/javascript-localstorage-expiration/).

## Files

| File | What it is |
| --- | --- |
| `ttl_storage.js` | `TTLStorage` class — set/get with expiry, quota retry, lazy cleanup, prefix-scoped `clearAll()`, in-memory fallback for private mode |
| `swr_storage.js` | `SWRStorage` class — stale-while-revalidate with `expiry` + `staleUntil` windows |
| `storage_mock.js` | Web Storage–compatible mock so the classes run under Node.js (tests, CI) |
| `ttl_storage.test.js` | `node:test` suite covering round-trip, lazy expiry, scoped cleanup, SWR states, and the memory fallback |
| `demo.html` | Browser demo — writes a key with a 5 s TTL and reads it back (ES modules, no bundler) |

## Run

```bash
node --test          # run the test suite (no dependencies)
npx serve .          # then open demo.html — modules need a server, not file://
```

## Notes

- Works in any browser with `localStorage`, and in Node.js by injecting a storage-compatible object (`new TTLStorage("app:", yourStorage)`).
- Expiration is lazy: expired entries are deleted on read or by `cleanup()` — nothing sweeps in the background.
- `Date.now()` follows the user's system clock; keep TTLs short enough that clock drift doesn't matter.
