# Service Worker Offline Caching en JavaScript

Código companion ejecutable de la [receta de StackPractices](https://stackpractices.com/es/recipes/javascript-service-worker-offline/).

## Archivos

| Archivo | Qué es |
| --- | --- |
| `sw.js` | El worker: precachea el app shell en `install`, limpia cachés viejas en `activate`, responde los GET con cache-first usando `offline.html` como respaldo de navegación, y reintenta los envíos encolados en `sync` |
| `main.js` | Lado de la página: registra `/sw.js`, muestra el estado de conexión y la cola local, envía el formulario con `SyncManager` cuando existe y con `fetch` directo si no |
| `db.js` | Cola IndexedDB compartida por la página (`<script>`) y el worker (`importScripts`) — `openDB`, `storeFormData`, `getStoredFormData`, `removeStoredFormData` |
| `index.html` | Página demo con formulario, estado online/offline en vivo y lista de envíos pendientes |
| `offline.html` | Página de respaldo con estilo que sirve el worker en las navegaciones sin conexión |
| `styles.css` | Estilos mínimos de la demo |
| `package.json` | `npm run demo` → `npx serve .` |

## Ejecutar

```bash
npm run demo     # o: npx serve .
# abre http://localhost:3000 (los service workers necesitan http(s), no file://)
```

## Probar el flujo offline

1. Carga la página una vez para que el worker se instale y precachee el shell.
2. DevTools → Network → marca **Offline** (o activa el modo avión).
3. Envía el formulario — la entrada cae en la cola de IndexedDB y queda listada.
4. Recarga sin conexión: la página sigue renderizando desde caché; los links directos resuelven a `offline.html`.
5. Vuelve online: Chrome dispara el evento `sync` y `replayFormSubmission()` hace POST de cada elemento encolado y lo borra.

## Notas

- `/api/submit` es un stub: en un servidor estático devuelve 404, así que `res.ok` falla, el evento sync reintenta después y el elemento queda en cola — es exactamente el camino de reintento que documenta la receta. Apúntalo a un endpoint real para ver la cola vaciarse.
- Background Sync (`SyncManager`) solo existe en Chromium; en Safari el envío recurre a un `fetch` plano, que rechaza sin conexión.
- Sube `CACHE_NAME` en `sw.js` para forzar un ciclo de actualización; DevTools → Application → Service Workers muestra el worker viejo en espera frente al nuevo activándose.
