# Rotación diaria de logs con Winston — Proyecto complementario

Complemento ejecutable de la receta de StackPractices [Rotar Logs Diariamente con Winston](https://stackpractices.com/es/recipes/nodejs-winston-daily-rotate/).

## Qué incluye

- `logger.js` — Winston configurado con dos transports `winston-daily-rotate-file` (info 14d + error 30d), `zippedArchive`, `auditFile`, listeners de eventos de rotación y un transport de consola solo para desarrollo.
- `server.js` — app Express que conecta el access log `combined` de morgan a Winston, con una ruta normal y una ruta de error forzado.
- `demo.js` — escribe una ráfaga de más de 100 entradas para que veas aparecer archivos en `logs/`.

## Ejecución

```bash
npm install
npm run demo      # escribe entradas en logs/application-*.log y logs/error-*.log
npm start         # Express en :3000 — visita /api/users/1 y /api/error
```

Revisa `logs/` para ver `application-YYYY-MM-DD.log`, `error-YYYY-MM-DD.log` y `audit.json`. Reduce `maxSize` (p. ej. `"1k"`) temporalmente si quieres observar una rotación en una sola ejecución.
