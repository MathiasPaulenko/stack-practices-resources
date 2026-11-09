#!/usr/bin/env python3
import boto3
import subprocess
import time
from dataclasses import dataclass, field
from typing import List, Optional
from datetime import datetime, timedelta

@dataclass
class DRTestResult:
    test_name: str
    start_time: datetime
    end_time: Optional[datetime] = None
    rto_seconds: Optional[int] = None
    rpo_seconds: Optional[int] = None
    steps_completed: List[str] = field(default_factory=list)
    steps_failed: List[str] = field(default_factory=list)
    data_integrity_ok: bool = False

class DRTestRunner:
    def __init__(self, region: str, dr_region: str):
        self.region = region
        self.dr_region = dr_region
        self.rds = boto3.client("rds", region_name=dr_region)
        self.ec2 = boto3.client("ec2", region_name=dr_region)
        self.s3 = boto3.client("s3", region_name=region)

    def restore_database_from_snapshot(
        self, snapshot_id: str, db_instance_id: str
    ) -> str:
        """Restore RDS instance from snapshot in DR region."""
        print(f"Restoring {db_instance_id} from snapshot {snapshot_id}...")
        response = self.rds.restore_db_instance_from_db_snapshot(
            DBInstanceIdentifier=db_instance_id,
            DBSnapshotIdentifier=snapshot_id,
            AvailabilityZone=f"{self.dr_region}a",
        )
        # Wait for instance to be available
        waiter = self.rds.get_waiter("db_instance_available")
        waiter.wait(DBInstanceIdentifier=db_instance_id)
        endpoint = response["DBInstance"]["Endpoint"]["Address"]
        print(f"Database available at: {endpoint}")
        return endpoint

    def run_smoke_tests(self, endpoint: str) -> bool:
        """Run smoke tests against the restored environment."""
        tests = [
            ("health_check", f"curl -sf http://{endpoint}/health"),
            ("write_test", f"curl -sf -X POST http://{endpoint}/api/test -d '{{\"test\":\"dr\"}}'"),
            ("read_test", f"curl -sf http://{endpoint}/api/test/dr"),
        ]
        all_passed = True
        for name, cmd in tests:
            result = subprocess.run(cmd, shell=True, capture_output=True, timeout=30)
            if result.returncode == 0:
                print(f"  PASS: {name}")
            else:
                print(f"  FAIL: {name}: {result.stderr.decode()}")
                all_passed = False
        return all_passed

    def verify_data_integrity(
        self, primary_conn: str, dr_conn: str
    ) -> bool:
        """Compare transaction counts between primary and DR."""
        primary_count = self._query_count(primary_conn)
        dr_count = self._query_count(dr_conn)
        match = primary_count == dr_count
        print(f"Primary: {primary_count} rows, DR: {dr_count} rows, Match: {match}")
        return match

    def _query_count(self, conn_str: str) -> int:
        """Execute a count query and return the result."""
        cmd = f'psql "{conn_str}" -t -c "SELECT COUNT(*) FROM orders;"'
        result = subprocess.run(cmd, shell=True, capture_output=True, timeout=60)
        return int(result.stdout.decode().strip()) if result.returncode == 0 else -1

    def execute_full_test(self, snapshot_id: str) -> DRTestResult:
        """Execute a full DR test and return results."""
        result = DRTestResult(
            test_name="full_region_failure",
            start_time=datetime.now(),
        )

        try:
            # Step 1: Restore database
            endpoint = self.restore_database_from_snapshot(
                snapshot_id, "dr-test-instance"
            )
            result.steps_completed.append("database_restore")

            # Step 2: Run smoke tests
            if self.run_smoke_tests(endpoint):
                result.steps_completed.append("smoke_tests")
            else:
                result.steps_failed.append("smoke_tests")

            # Step 3: Verify data integrity
            if self.verify_data_integrity(
                "postgresql://primary.db.internal/appdb",
                f"postgresql://{endpoint}/appdb",
            ):
                result.data_integrity_ok = True
                result.steps_completed.append("data_integrity")
            else:
                result.steps_failed.append("data_integrity")

        except Exception as e:
            print(f"Test failed: {e}")
            result.steps_failed.append(f"exception: {str(e)}")

        result.end_time = datetime.now()
        result.rto_seconds = int((result.end_time - result.start_time).total_seconds())
        return result

# Example usage
runner = DRTestRunner("us-east-1", "us-west-2")
result = runner.execute_full_test("rds-snapshot-2026-07-01")
print(f"\nRTO: {result.rto_seconds}s")
print(f"Steps completed: {result.steps_completed}")
print(f"Steps failed: {result.steps_failed}")
print(f"Data integrity: {result.data_integrity_ok}")
