"""Security group auditor: finds overly permissive rules and exports a CSV.

Source article: https://stackpractices.com/docs/network-security-template/

Requires: boto3 and AWS credentials with ec2:DescribeSecurityGroups.
Usage: python sg_audit.py [--region us-east-1] [--output sg-audit-report.csv]
"""

import argparse
import csv
import json
from dataclasses import asdict, dataclass
from typing import List

import boto3


@dataclass
class SecurityGroupFinding:
    group_id: str
    group_name: str
    direction: str  # ingress or egress
    protocol: str
    from_port: int
    to_port: int
    cidr: str
    severity: str  # critical / warning / ok
    vpc_id: str


class SecurityGroupAuditor:
    def __init__(self, region: str = "us-east-1"):
        self.ec2 = boto3.client("ec2", region_name=region)

    def audit_all_security_groups(self) -> List[SecurityGroupFinding]:
        """Audit every security group rule and assign a severity."""
        findings = []
        response = self.ec2.describe_security_groups()

        for sg in response["SecurityGroups"]:
            for rule_type in ["IpPermissions", "IpPermissionsEgress"]:
                direction = "ingress" if rule_type == "IpPermissions" else "egress"
                for rule in sg.get(rule_type, []):
                    for ip_range in rule.get("IpRanges", []):
                        cidr = ip_range.get("CidrIp", "N/A")
                        from_port = rule.get("FromPort", 0)
                        # 0.0.0.0/0 inbound on non-web ports is critical;
                        # 0.0.0.0/0 on web ports or outbound is a warning.
                        if cidr != "0.0.0.0/0":
                            severity = "ok"
                        elif direction == "ingress" and from_port not in (80, 443):
                            severity = "critical"
                        else:
                            severity = "warning"

                        findings.append(
                            SecurityGroupFinding(
                                group_id=sg["GroupId"],
                                group_name=sg["GroupName"],
                                direction=direction,
                                protocol=rule.get("IpProtocol", "all"),
                                from_port=from_port,
                                to_port=rule.get("ToPort", 0),
                                cidr=cidr,
                                severity=severity,
                                vpc_id=sg.get("VpcId", "default"),
                            )
                        )
        return findings

    def export_findings(self, findings: List[SecurityGroupFinding], output_file: str) -> None:
        """Export findings to CSV for the audit trail."""
        with open(output_file, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow([
                "Group ID", "Group Name", "Direction", "Protocol",
                "From Port", "To Port", "CIDR", "Severity", "VPC ID",
            ])
            for finding in findings:
                writer.writerow([
                    finding.group_id, finding.group_name, finding.direction,
                    finding.protocol, finding.from_port, finding.to_port,
                    finding.cidr, finding.severity, finding.vpc_id,
                ])


def main() -> None:
    parser = argparse.ArgumentParser(description="Audit security groups for permissive rules")
    parser.add_argument("--region", default="us-east-1")
    parser.add_argument("--output", default="sg-audit-report.csv")
    args = parser.parse_args()

    auditor = SecurityGroupAuditor(region=args.region)
    findings = auditor.audit_all_security_groups()
    auditor.export_findings(findings, args.output)

    critical = [f for f in findings if f.severity == "critical"]
    print(f"Total rules: {len(findings)}")
    print(f"Critical rules: {len(critical)}")
    for r in critical:
        print(
            f"  RISK: {r.group_name} ({r.direction})"
            f" - {r.protocol}:{r.from_port} from {r.cidr}"
        )

    with open("sg-audit-report.json", "w") as f:
        json.dump([asdict(x) for x in findings], f, indent=2)


if __name__ == "__main__":
    main()
