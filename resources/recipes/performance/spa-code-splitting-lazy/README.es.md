# Code Splitting y Lazy Loading en SPA — Companion

App Vite + React ejecutable que demuestra code splitting a nivel de ruta con
`React.lazy`/`Suspense`, prefetch al pasar el cursor, un error boundary para
chunks y `manualChunks` para separar el vendor.

## Ejecutar

```bash
npm install
npm run dev
npm run build   # inspecciona dist/assets para ver los chunks emitidos
```

## Qué mirar

- `src/App.tsx` — rutas lazy dentro de una barrera `Suspense` envuelta por `ChunkErrorBoundary`
- `src/utils/prefetch.ts` — prefetch al pasar el cursor que calienta la caché antes de navegar
- `src/components/ChunkErrorBoundary.tsx` — captura fallos de chunks obsoletos tras un redeploy
- `vite.config.ts` — `manualChunks` separa `react`, `react-dom` y `react-router-dom` en un chunk vendor

Receta original: <https://stackpractices.com/es/recipes/spa-code-splitting-lazy/>
