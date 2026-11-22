# Node.js In-Memory LRU Cache — Companion Code

Runnable companion for the [StackPractices recipe](https://stackpractices.com/recipes/nodejs-in-memory-cache-lru/).

## Files

| File | What it shows |
| --- | --- |
| `lru-dll.ts` | Textbook LRU: `Map` for O(1) lookup + doubly linked list for O(1) move/evict |
| `lru-map.ts` | Map-only LRU (`delete` + `set`) for small caches |
| `ttl-cache.ts` | LRU with per-entry TTL and a periodic sweeper (full-scan `cleanup`) |
| `async-lru.ts` | Async LRU storing promises; rejections delete themselves instead of poisoning the entry |
| `benchmark.js` | Eviction-cost comparison between both implementations at growing capacities |

## Run

```bash
npx tsc lru-dll.ts lru-map.ts ttl-cache.ts async-lru.ts --target es2020 --module commonjs
node benchmark.js
```

Expect the Map-only version to slow down on eviction as capacity grows into the
tens of thousands, while the linked-list version stays flat.

## Which one should I use?

- A few hundred keys, readability first → `lru-map.ts`
- Frequent evictions or thousands of keys → `lru-dll.ts`
- Production with TTL, `dispose`, byte-size limits → the [`lru-cache`](https://github.com/isaacs/node-lru-cache) package
