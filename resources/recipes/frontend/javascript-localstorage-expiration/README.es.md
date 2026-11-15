# LocalStorage con Expiración TTL en JavaScript

Código companion ejecutable de la [receta de StackPractices](https://stackpractices.com/es/recipes/javascript-localstorage-expiration/).

## Archivos

| Archivo | Qué es |
| --- | --- |
| `ttl_storage.js` | Clase `TTLStorage` — set/get con expiración, reintento de cuota, limpieza perezosa, `clearAll()` acotado al prefijo y respaldo en memoria para modo privado |
| `swr_storage.js` | Clase `SWRStorage` — stale-while-revalidate con ventanas `expiry` + `staleUntil` |
| `storage_mock.js` | Mock compatible con Web Storage para que las clases corran en Node.js (tests, CI) |
| `ttl_storage.test.js` | Suite `node:test`: ida y vuelta, expiración perezosa, limpieza acotada, estados SWR y respaldo en memoria |
| `demo.html` | Demo en el navegador — escribe una clave con TTL de 5 s y la lee a pedido (módulos ES, sin bundler) |

## Ejecutar

```bash
node --test          # corre la suite de tests (sin dependencias)
npx serve .          # luego abre demo.html — los módulos necesitan servidor, no file://
```

## Notas

- Funciona en cualquier navegador con `localStorage`, y en Node.js inyectando un objeto compatible (`new TTLStorage("app:", tuStorage)`).
- La expiración es perezosa: las entradas expiradas se borran al leerlas o con `cleanup()` — nada barre en segundo plano.
- `Date.now()` sigue el reloj del sistema del usuario; mantén los TTL lo bastante cortos para que la deriva no importe.
