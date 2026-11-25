# Race Condition Prevention — Companion

Runnable versions of the six patterns from the
[race condition prevention recipe](https://stackpractices.com/recipes/race-condition-prevention/).
Each file maps to a numbered solution in the recipe.

## Files

| File | Pattern | What it prevents |
|------|---------|------------------|
| `search_service.ts` | AbortController | A stale response overwriting a newer query's results |
| `atomic_counter.ts` | Serialized promise queue | Lost increments across `await` boundaries |
| `use_latest_query.ts` | Request IDs (latest-only) | Rendering the loser of an out-of-order race |
| `mutex.ts` | FIFO mutex | Check-and-act interleaving on shared state |
| `cas_store.ts` | Compare-and-swap | Blind writes; retry only when the value moved |
| `asyncio_transfer.py` | `asyncio.Lock` | The same check-and-act race in Python services |

## Run them

```bash
python asyncio_transfer.py          # A: 600, B: 900 — every transfer serialized
npx tsx mutex.ts                    # TypeScript files run with tsx/ts-node
```

## Notes

- `asyncio_transfer.py` needs Python 3.8+, no dependencies.
- The `.ts` files are self-contained snippets: `use_latest_query.ts` expects
  React (a `useCallback`/`useRef` hook); the rest are framework-free.
- Single-threaded doesn't mean race-free: every `await` is a yield point
  where another task can interleave between your check and your write.
