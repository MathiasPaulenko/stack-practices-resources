import time
import boto3
from dataclasses import dataclass
from typing import List, Tuple

@dataclass
class ReachabilityTest:
    source_instance: str
    destination_ip: str
    destination_port: int
    expected_result: str  # "allow" or "deny"
    zone_pair: str  # e.g., "DMZ -> Application"

class NetworkReachabilityValidator:
    def __init__(self, region: str = "us-east-1"):
        self.ssm = boto3.client("ssm", region_name=region)

    def run_test(self, test: ReachabilityTest) -> Tuple[bool, str]:
        """Run a single reachability test via SSM."""
        try:
            response = self.ssm.send_command(
                InstanceIds=[test.source_instance],
                DocumentName="AWS-RunShellScript",
                Parameters={
                    "commands": [
                        f"timeout 5 bash -c 'echo > /dev/tcp/{test.destination_ip}/{test.destination_port}' "
                        f"2>/dev/null && echo 'REACHABLE' || echo 'UNREACHABLE'"
                    ]
                },
            )
            command_id = response["Command"]["CommandId"]

            time.sleep(5)

            output = self.ssm.get_command_invocation(
                CommandId=command_id,
                InstanceId=test.source_instance,
            )

            actual = "allow" if "REACHABLE" in output.get("StandardOutputContent", "") else "deny"
            passed = actual == test.expected_result
            status = "PASS" if passed else "FAIL"
            message = f"{status}: {test.zone_pair} - Expected {test.expected_result}, got {actual}"
            return passed, message
        except Exception as e:
            return False, f"ERROR: {test.zone_pair} - {str(e)}"

    def validate_segmentation(self, tests: List[ReachabilityTest]) -> None:
        """Run all reachability tests and report results."""
        passed = 0
        failed = 0
        for test in tests:
            ok, msg = self.run_test(test)
            print(msg)
            if ok:
                passed += 1
            else:
                failed += 1
        print(f"\nResults: {passed} passed, {failed} failed out of {len(tests)} tests")

# Example usage
tests = [
    ReachabilityTest("i-dmz001", "10.0.2.10", 443, "allow", "DMZ -> Application"),
    ReachabilityTest("i-dmz001", "10.0.3.10", 5432, "deny", "DMZ -> Data"),
    ReachabilityTest("i-app001", "10.0.3.10", 5432, "allow", "Application -> Data"),
    ReachabilityTest("i-dev001", "10.0.3.10", 5432, "deny", "Development -> Data"),
]

validator = NetworkReachabilityValidator(region="us-east-1")
validator.validate_segmentation(tests)
