"""Automated backup integrity check: restore the latest backup to a throwaway
instance and verify it actually contains data.

Requires: pg_restore and psql on PATH, plus a scratch Postgres instance
(e.g. a disposable container). Configure via environment variables.
"""
import os
import subprocess
import sys

RESTORE_DB = os.environ.get("RESTORE_DB", "dr_restore_test")
PGHOST = os.environ.get("PGHOST", "localhost")
PGUSER = os.environ.get("PGUSER", "postgres")
BACKUP_DIR = os.environ.get("BACKUP_DIR", "/backups")
CRITICAL_TABLE = os.environ.get("CRITICAL_TABLE", "critical_table")


def latest_backup() -> str:
    dumps = sorted(
        d for d in os.listdir(BACKUP_DIR) if d.startswith("20")
    )
    if not dumps:
        sys.exit("No backups found in " + BACKUP_DIR)
    return os.path.join(BACKUP_DIR, dumps[-1])


def run(cmd: list[str]) -> subprocess.CompletedProcess:
    return subprocess.run(cmd, capture_output=True, text=True)


def main() -> int:
    backup = latest_backup()
    print(f"Restoring {backup} into {RESTORE_DB}...")

    run(["dropdb", "--if-exists", "-h", PGHOST, "-U", PGUSER, RESTORE_DB])
    created = run(["createdb", "-h", PGHOST, "-U", PGUSER, RESTORE_DB])
    if created.returncode != 0:
        print("createdb failed:", created.stderr.strip())
        return 1

    restored = run([
        "pg_restore", "-h", PGHOST, "-U", PGUSER,
        "-d", RESTORE_DB, backup,
    ])
    if restored.returncode != 0:
        print("pg_restore failed:", restored.stderr.strip())
        return 1

    count = run([
        "psql", "-h", PGHOST, "-U", PGUSER, "-d", RESTORE_DB,
        "-tAc", f"SELECT count(*) FROM {CRITICAL_TABLE}",
    ])
    rows = count.stdout.strip()
    if count.returncode != 0 or not rows.isdigit() or int(rows) == 0:
        print(f"Restored DB appears empty or broken ({CRITICAL_TABLE}: {rows!r})")
        return 1

    print(f"OK: {CRITICAL_TABLE} has {rows} rows. Backup verified.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
