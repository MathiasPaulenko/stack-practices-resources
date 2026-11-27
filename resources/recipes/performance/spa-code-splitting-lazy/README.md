# SPA Code Splitting and Lazy Loading — Companion

Runnable Vite + React app demonstrating route-level code splitting with
`React.lazy`/`Suspense`, prefetch-on-hover, a chunk error boundary, and
`manualChunks` vendor splitting.

## Run

```bash
npm install
npm run dev
npm run build   # inspect dist/assets to see the emitted chunks
```

## What to look at

- `src/App.tsx` — lazy routes inside a `Suspense` boundary wrapped by `ChunkErrorBoundary`
- `src/utils/prefetch.ts` — hover prefetch that warms the module cache before navigation
- `src/components/ChunkErrorBoundary.tsx` — catches stale-chunk failures after a redeploy
- `vite.config.ts` — `manualChunks` pulls `react`, `react-dom`, `react-router-dom` into a shared vendor chunk

Source recipe: <https://stackpractices.com/recipes/spa-code-splitting-lazy/>
