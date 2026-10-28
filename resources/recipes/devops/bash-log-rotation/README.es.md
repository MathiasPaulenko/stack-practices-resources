# Rotación y Compresión de Logs en Bash

Archivos complementarios de la [receta de rotación de logs](https://stackpractices.com/es/recipes/bash-log-rotation/) en StackPractices.

- `logrotate-*.conf` — configs listas para `/etc/logrotate.d/` (gzip, por tamaño, zstd, copytruncate, email)
- `*.sh` — scripts de rotación propios para hosts sin logrotate (por tamaño, por señal, pigz, chequeo de disco, envío a S3)
- `python-rotating-handler.py` — rotación desde la app con compresión gzip

Prueba las configs con `logrotate -d <archivo>` antes de desplegar. Un `find -delete` mal puesto se come logs en vivo.

## Licencia

MIT
