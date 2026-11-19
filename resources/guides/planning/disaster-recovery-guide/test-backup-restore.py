"""Restore the newest logical PostgreSQL dump into a disposable database.

The companion backup script also creates a physical pg_basebackup archive.
That cluster archive is a different format and must not be passed to pg_restore.
This check restores only the matching custom-format .dump file and verifies a
configured table. It does not simulate physical cluster recovery or WAL replay.
"""
import os
import re
import subprocess
import sys
from pathlib import Path

RESTORE_DB = os.environ.get("RESTORE_DB", "dr_restore_test")
PGHOST = os.environ.get("PGHOST", "localhost")
PGUSER = os.environ.get("PGUSER", "postgres")
BACKUP_DIR = Path(os.environ.get("BACKUP_DIR", "/backups"))
BACKUP_FILE = os.environ.get("BACKUP_FILE")
CRITICAL_TABLE = os.environ.get("CRITICAL_TABLE", "public.critical_table")


def latest_backup() -> Path:
    if BACKUP_FILE:
        backup = Path(BACKUP_FILE)
        if not backup.is_absolute():
            backup = BACKUP_DIR / backup
        if not backup.is_file() or backup.suffix != ".dump":
            sys.exit("BACKUP_FILE must point to an existing custom-format .dump file")
        return backup

    dumps = list(BACKUP_DIR.glob("*.dump"))
    if not dumps:
        sys.exit("No logical .dump files found in " + str(BACKUP_DIR))
    return max(dumps, key=lambda path: (path.stat().st_mtime, path.name))


def run(cmd: list[str]) -> subprocess.CompletedProcess:
    return subprocess.run(cmd, capture_output=True, text=True)


def quote_table_name(value: str) -> str:
    parts = value.split(".")
    if len(parts) not in (1, 2) or any(
        not re.fullmatch(r"[A-Za-z_][A-Za-z0-9_]*", part) for part in parts
    ):
        sys.exit("CRITICAL_TABLE must be table or schema.table using SQL identifiers")
    return ".".join(f'"{part}"' for part in parts)


def main() -> int:
    backup = latest_backup()
    table = quote_table_name(CRITICAL_TABLE)
    print(f"Restoring logical archive {backup} into disposable database {RESTORE_DB}...")

    dropped = run(["dropdb", "--if-exists", "-h", PGHOST, "-U", PGUSER, RESTORE_DB])
    if dropped.returncode != 0:
        print("dropdb failed:", dropped.stderr.strip())
        return 1

    created = run(["createdb", "-h", PGHOST, "-U", PGUSER, RESTORE_DB])
    if created.returncode != 0:
        print("createdb failed:", created.stderr.strip())
        return 1

    restored = run([
        "pg_restore", "--exit-on-error", "--no-owner",
        "-h", PGHOST, "-U", PGUSER, "-d", RESTORE_DB, str(backup),
    ])
    if restored.returncode != 0:
        run(["dropdb", "--if-exists", "-h", PGHOST, "-U", PGUSER, RESTORE_DB])
        print("pg_restore failed:", restored.stderr.strip())
        return 1

    count = run([
        "psql", "-h", PGHOST, "-U", PGUSER, "-d", RESTORE_DB,
        "-v", "ON_ERROR_STOP=1", "-tAc",
        f"SELECT count(*) FROM {table}",
    ])
    rows = count.stdout.strip()
    if count.returncode != 0 or not rows.isdigit() or int(rows) == 0:
        run(["dropdb", "--if-exists", "-h", PGHOST, "-U", PGUSER, RESTORE_DB])
        print(f"Restored database appears empty or broken ({table}: {rows!r})")
        if count.returncode != 0:
            print(count.stderr.strip())
        return 1

    print(f"OK: {table} has {rows} rows. Logical restore verified.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
