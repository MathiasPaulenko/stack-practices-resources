# Bash Backup Rotation: Retention and Integrity

Companion scripts for the [Bash Backup Rotation](https://stackpractices.com/recipes/bash-backup-rotation-script/) recipe on StackPractices.

Each `.sh` file is self-contained: adjust the variables at the top and run it. Scripts use `set -euo pipefail` so a failed pipeline stops the run instead of pruning good backups.

## Prerequisites

- GNU bash and GNU tar (`pigz` optional for parallel compression — `tar -I` is GNU-only)
- `gpg` for `encrypted-backup-gpg.sh`, `rsync` for the incremental variant, `pg_dump` for the database variant
- A `~/.pgpass` entry (or `PGUSER`/peer auth) so `pg_dump` never prompts inside cron

## Scripts

| File | What it does |
| --- | --- |
| `backup-rotation.sh` | Daily/weekly/monthly (GFS) rotation with temp-publish and list-test before pruning |
| `encrypted-backup-gpg.sh` | Tars and encrypts in one pipeline, verifies packet headers before pruning |
| `incremental-backup-rsync.sh` | Dated snapshots sharing unchanged files via `--link-dest` |
| `s3-upload-checksum.sh` | Uploads to S3 with SHA-256 checksum validation and metadata |
| `backup-integrity-check.sh` | Read-tests archives (`tar -tzf`) and reports corrupt files |
| `database-backup-pg-dump.sh` | `pg_dump | gzip` rotation with pipefail + `gzip -t` + 14-day prune |
| `restore-backup.sh` | Extracts an archive (or .gpg) into an empty dir for inspection |
| `disk-space-check.sh` | POSIX `df -kP` + `du -sk` pre-flight before writing the archive |
| `performance-tips.sh` | `pigz`, `--exclude` lists, and `ionice` snippets for large trees |

## Scheduling

```cron
0 2 * * * /opt/scripts/backup-rotation.sh >> /var/log/backup.log 2>&1
```

## License

MIT — same as the StackPractices resources repository.
