# Monitoreo de Usuarios Reales (RUM) con web-vitals

Código companion de la receta de StackPractices:
<https://stackpractices.com/es/recipes/real-user-monitoring/>

Recolecta Core Web Vitals de navegadores reales, envíalos con `sendBeacon` y añade session replay encima.

## Archivos

| Archivo | Stack | Qué muestra |
| --- | --- | --- |
| `vitals-collector.js` | web-vitals v4 | `onCLS`/`onINP`/`onFCP`/`onLCP`/`onTTFB` con `sendBeacon` y fallback a `fetch` |
| `sentry-replay.js` | `@sentry/browser` | `replayIntegration()` con enmascarado de privacidad y sampling por sesión |
| `performance-observer.js` | PerformanceObserver | Métricas personalizadas: recursos lentos y long tasks |
| `ingest-server.js` | Node.js | Endpoint de beacons mínimo que registra vitals como JSONL |

## Ejecutar

```bash
npm install
npm run ingest   # endpoint /analytics/vitals mínimo en :8899
```

Importa `vitals-collector.js` (y opcionalmente `sentry-replay.js` y `performance-observer.js`) desde el punto de entrada de tu app. Reemplaza `/analytics/vitals` y el DSN de Sentry por tus propios valores.

## Notas

- `web-vitals` v4 reporta INP (FID se retiró de Core Web Vitals en marzo de 2024).
- El paquete independiente `@sentry/replay` está deprecado; desde el SDK v7, replay viene en `@sentry/browser`.
- `sendBeacon` mantiene los eventos vivos cuando el usuario cierra la pestaña en medio de una medición.
- Muestrea el replay al ~1% de las sesiones (100% en sesiones con error) — pesa más que los vitals.
