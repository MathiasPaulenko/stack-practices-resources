"""Delete manual RDS snapshots older than N days.

Automated snapshots can't be deleted directly — they expire with their
retention period — so filter SnapshotType='manual' server-side.
Run from a scheduled Lambda or cron host with rds:DeleteDBSnapshot.
"""

import boto3
from datetime import datetime, timedelta, timezone

rds = boto3.client("rds")


def cleanup_old_snapshots(days=30):
    cutoff = datetime.now(timezone.utc) - timedelta(days=days)
    paginator = rds.get_paginator("describe_db_snapshots")

    for page in paginator.paginate(SnapshotType="manual"):
        for snap in page["DBSnapshots"]:
            if snap["SnapshotCreateTime"] >= cutoff:
                continue
            try:
                rds.delete_db_snapshot(
                    DBSnapshotIdentifier=snap["DBSnapshotIdentifier"]
                )
                print(f"Deleted: {snap['DBSnapshotIdentifier']}")
            except rds.exceptions.InvalidDBSnapshotStateException:
                continue  # snapshot in use or being copied


if __name__ == "__main__":
    cleanup_old_snapshots()
