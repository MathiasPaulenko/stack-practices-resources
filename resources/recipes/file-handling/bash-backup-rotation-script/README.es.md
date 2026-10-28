# Rotación de backups en Bash: retención e integridad

Scripts complementarios de la receta [Rotación de backups en Bash](https://stackpractices.com/es/recipes/bash-backup-rotation-script/) en StackPractices.

Cada `.sh` es autocontenido: ajusta las variables de arriba y ejecútalo. Usan `set -euo pipefail` para que un pipeline fallido detenga el run en vez de podar backups buenos.

## Requisitos

- GNU bash y GNU tar (`pigz` opcional — `tar -I` es solo GNU)
- `gpg` para `encrypted-backup-gpg.sh`, `rsync` para la variante incremental, `pg_dump` para la de base de datos
- Una entrada en `~/.pgpass` (o auth `PGUSER`/peer) para que `pg_dump` no pida contraseña dentro de cron

## Scripts

| Archivo | Qué hace |
| --- | --- |
| `backup-rotation.sh` | Rotación diaria/semanal/mensual (GFS) con publicación temporal y test antes de podar |
| `encrypted-backup-gpg.sh` | Comprime y cifra en un pipeline, verifica cabeceras antes de podar |
| `incremental-backup-rsync.sh` | Snapshots por fecha que comparten archivos con `--link-dest` |
| `s3-upload-checksum.sh` | Subida a S3 con checksum SHA-256 y metadata |
| `backup-integrity-check.sh` | Testea archivos con `tar -tzf` y reporta los corruptos |
| `database-backup-pg-dump.sh` | `pg_dump | gzip` con pipefail + `gzip -t` + poda a 14 días |
| `restore-backup.sh` | Extrae un archivo (o .gpg) en un directorio vacío para inspección |
| `disk-space-check.sh` | Chequeo POSIX `df -kP` + `du -sk` antes de escribir el archivo |
| `performance-tips.sh` | `pigz`, listas `--exclude` e `ionice` para árboles grandes |

## Programación

```cron
0 2 * * * /opt/scripts/backup-rotation.sh >> /var/log/backup.log 2>&1
```

## Licencia

MIT — igual que el repositorio stack-practices-resources.
