# Log Rotation and Compression in Bash

Companion files for the [log rotation recipe](https://stackpractices.com/recipes/bash-log-rotation/) on StackPractices.

- `logrotate-*.conf` — drop-in configs for `/etc/logrotate.d/` (gzip, size-based, zstd, copytruncate, email notify)
- `*.sh` — custom rotation scripts for hosts without logrotate (size-based, signal, pigz, disk-check, S3 shipping)
- `python-rotating-handler.py` — in-app rotation with gzip compression

Test logrotate configs with `logrotate -d <file>` before deploying. Keep a shell session open — a bad `find -delete` eats live logs.

## License

MIT
