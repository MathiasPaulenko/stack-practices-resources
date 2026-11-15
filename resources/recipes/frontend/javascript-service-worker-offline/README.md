# JavaScript Service Worker Offline Caching

Runnable companion code for the [StackPractices recipe](https://stackpractices.com/recipes/javascript-service-worker-offline/).

## Files

| File | What it is |
| --- | --- |
| `sw.js` | The worker: precaches the app shell on `install`, cleans old caches on `activate`, answers GETs cache-first with `offline.html` as the navigation fallback, and replays queued submissions on `sync` |
| `main.js` | Page side: registers `/sw.js`, renders connection status and the local queue, submits the form through `SyncManager` when available with a direct `fetch` fallback |
| `db.js` | IndexedDB queue shared by the page (`<script>`) and the worker (`importScripts`) — `openDB`, `storeFormData`, `getStoredFormData`, `removeStoredFormData` |
| `index.html` | Demo page with a form, live online/offline status and the pending-submission list |
| `offline.html` | Styled fallback page served by the worker for navigations while offline |
| `styles.css` | Minimal demo styles |
| `package.json` | `npm run demo` → `npx serve .` |

## Run

```bash
npm run demo     # or: npx serve .
# open http://localhost:3000 (service workers need http(s), not file://)
```

## Try the offline flow

1. Load the page once so the worker installs and precaches the shell.
2. DevTools → Network → check **Offline** (or enable airplane mode).
3. Submit the form — the entry lands in the IndexedDB queue and stays listed.
4. Reload while offline: the page still renders from cache; direct links resolve to `offline.html`.
5. Go back online: Chrome fires the `sync` event and `replayFormSubmission()` POSTs each queued item, then removes it.

## Notes

- `/api/submit` is a stub: on a static server it returns 404, so `res.ok` fails, the sync event retries later, and the item stays queued — that is the retry path the recipe documents. Point it at a real endpoint to see items drain.
- Background Sync (`SyncManager`) is Chromium-only; on Safari the submit path falls back to a plain `fetch`, which rejects while offline.
- Bump `CACHE_NAME` in `sw.js` to force an update cycle; DevTools → Application → Service Workers shows the old worker waiting vs. the new one activating.
