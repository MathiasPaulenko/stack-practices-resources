#!/usr/bin/env python3
import boto3
import json
import os
import subprocess
import urllib.error
import urllib.request
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import List, Optional

@dataclass
class DRTestResult:
    test_name: str
    start_time: datetime
    end_time: Optional[datetime] = None
    rto_seconds: Optional[int] = None
    rpo_seconds: Optional[int] = None
    steps_completed: List[str] = field(default_factory=list)
    steps_failed: List[str] = field(default_factory=list)
    row_counts_match: bool = False

class DRTestRunner:
    def __init__(self, dr_region: str):
        self.dr_region = dr_region
        self.rds = boto3.client("rds", region_name=dr_region)

    def restore_database_from_snapshot(
        self, snapshot_id: str, db_instance_id: str, db_subnet_group: str
    ) -> str:
        """Restore a snapshot that is already available in the DR region."""
        print(f"Restoring {db_instance_id} from snapshot {snapshot_id}...")
        self.rds.restore_db_instance_from_db_snapshot(
            DBInstanceIdentifier=db_instance_id,
            DBSnapshotIdentifier=snapshot_id,
            DBSubnetGroupName=db_subnet_group,
        )
        waiter = self.rds.get_waiter("db_instance_available")
        waiter.wait(DBInstanceIdentifier=db_instance_id)
        response = self.rds.describe_db_instances(
            DBInstanceIdentifier=db_instance_id
        )
        endpoint = response["DBInstances"][0]["Endpoint"]["Address"]
        print(f"Database available at: {endpoint}")
        return endpoint

    def run_smoke_tests(self, app_base_url: str) -> bool:
        """Call application routes; an RDS endpoint is not an HTTP URL."""
        test_url = f"{app_base_url.rstrip('/')}/api/test/dr-test"
        tests = [
            ("health_check", f"{app_base_url.rstrip('/')}/health", "GET", None),
            ("write_test", test_url, "POST", {"test_id": "dr-test"}),
            ("read_test", test_url, "GET", None),
        ]
        all_passed = True
        for name, url, method, payload in tests:
            body = json.dumps(payload).encode("utf-8") if payload else None
            request = urllib.request.Request(
                url,
                data=body,
                method=method,
                headers={"Content-Type": "application/json"},
            )
            try:
                with urllib.request.urlopen(request, timeout=30) as response:
                    passed = 200 <= response.status < 300
            except (urllib.error.URLError, TimeoutError) as error:
                print(f"  FAIL: {name}: {error}")
                all_passed = False
                continue
            if passed:
                print(f"  PASS: {name}")
            else:
                print(f"  FAIL: {name}: HTTP {response.status}")
                all_passed = False
        return all_passed

    def verify_data_integrity(
        self, primary_conn: str, dr_conn: str
    ) -> bool:
        """Compare counts as a smoke check, not as proof of row equality."""
        primary_count = self._query_count(primary_conn)
        dr_count = self._query_count(dr_conn)
        match = primary_count is not None and primary_count == dr_count
        print(f"Primary: {primary_count} rows, DR: {dr_count} rows, Match: {match}")
        return match

    def _query_count(self, conn_str: str) -> Optional[int]:
        """Execute a count query and return the result."""
        result = subprocess.run(
            ["psql", conn_str, "-t", "-c", "SELECT COUNT(*) FROM orders;"],
            capture_output=True,
            text=True,
            timeout=60,
            check=False,
        )
        return int(result.stdout.strip()) if result.returncode == 0 else None

    def execute_full_test(
        self,
        snapshot_id: str,
        db_subnet_group: str,
        app_base_url: str,
        primary_database_url: str,
        dr_database_url: str,
    ) -> DRTestResult:
        """Execute a full DR test and return results."""
        result = DRTestResult(
            test_name="full_region_failure",
            start_time=datetime.now(timezone.utc),
        )

        try:
            # Step 1: Restore database
            self.restore_database_from_snapshot(
                snapshot_id, "dr-test-instance", db_subnet_group
            )
            result.steps_completed.append("database_restore")

            # Step 2: Run smoke tests
            if self.run_smoke_tests(app_base_url):
                result.steps_completed.append("smoke_tests")
                result.rto_seconds = int(
                    (datetime.now(timezone.utc) - result.start_time).total_seconds()
                )
            else:
                result.steps_failed.append("smoke_tests")

            # Step 3: Verify data integrity
            if self.verify_data_integrity(
                primary_database_url,
                dr_database_url,
            ):
                result.row_counts_match = True
                result.steps_completed.append("data_integrity")
            else:
                result.steps_failed.append("data_integrity")

        except Exception as e:
            print(f"Test failed: {e}")
            result.steps_failed.append(f"exception: {str(e)}")

        result.end_time = datetime.now(timezone.utc)
        return result

# Example usage
runner = DRTestRunner(dr_region="us-west-2")
result = runner.execute_full_test(
    snapshot_id=os.environ["DR_SNAPSHOT_ID"],
    db_subnet_group=os.environ["DR_DB_SUBNET_GROUP"],
    app_base_url=os.environ["DR_APP_BASE_URL"],
    primary_database_url=os.environ["PRIMARY_DATABASE_URL"],
    dr_database_url=os.environ["DR_DATABASE_URL"],
)
print(f"\nRTO: {result.rto_seconds}s")
print(f"RPO: {result.rpo_seconds} (not calculated by this example)")
print(f"Steps completed: {result.steps_completed}")
print(f"Steps failed: {result.steps_failed}")
print(f"Row counts match: {result.row_counts_match}")
