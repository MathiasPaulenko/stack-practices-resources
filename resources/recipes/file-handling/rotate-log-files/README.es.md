# Rotar Archivos de Log

Ejemplos complementarios de la [receta Rotar Archivos de Log](https://stackpractices.com/es/recipes/rotate-log-files/) en StackPractices.

## Archivos

- `python_rotation.py` — `RotatingFileHandler` (tamaño), `TimedRotatingFileHandler` (diario), `WatchedFileHandler` (compatible con logrotate).
- `python_json_rotation.py` — formateador JSON sobre un handler rotativo.
- `nodejs_winston_rotation.js` — transport `File` de Winston más `winston-daily-rotate-file` con `zippedArchive` y `maxFiles: '30d'`. Requiere `npm install winston winston-daily-rotate-file`.
- `logback.xml` — `RollingFileAppender` con `SizeAndTimeBasedRollingPolicy`, `maxFileSize`, `maxHistory`, `totalSizeCap`.
- `logrotate-daily.conf` — entrada diaria de `logrotate` con `postrotate` + `SIGHUP`.
- `logrotate-size.conf` — entrada por tamaño de `logrotate` con `copytruncate`.
- `logrotate-zstd.conf` — `logrotate` con compresión zstd (requiere logrotate 3.18+).

## Notas

Elige una sola capa de rotación por archivo: la app, `logrotate` o el runtime de contenedores. Combinar dos sobre el mismo archivo produce archivos truncados y líneas perdidas.
