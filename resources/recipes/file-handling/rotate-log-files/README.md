# Rotate Log Files

Companion examples for the [Rotate Log Files recipe](https://stackpractices.com/recipes/rotate-log-files/) on StackPractices.

## Files

- `python_rotation.py` — `RotatingFileHandler` (size), `TimedRotatingFileHandler` (daily), `WatchedFileHandler` (logrotate-compatible).
- `python_json_rotation.py` — JSON formatter on a rotating handler.
- `nodejs_winston_rotation.js` — Winston `File` transport plus `winston-daily-rotate-file` with `zippedArchive` and `maxFiles: '30d'`. Requires `npm install winston winston-daily-rotate-file`.
- `logback.xml` — `RollingFileAppender` with `SizeAndTimeBasedRollingPolicy`, `maxFileSize`, `maxHistory`, `totalSizeCap`.
- `logrotate-daily.conf` — daily `logrotate` entry with `postrotate` + `SIGHUP`.
- `logrotate-size.conf` — size-based `logrotate` entry with `copytruncate`.
- `logrotate-zstd.conf` — `logrotate` with zstd compression (requires logrotate 3.18+).

## Notes

Pick one rotation layer per file: the app, `logrotate`, or the container runtime. Combining two on the same file produces truncated archives and lost lines.
