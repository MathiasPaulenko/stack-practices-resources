# Network Security Template

A network security inventory template plus the automation scripts from the article: a security group auditor, a VPC flow log analyzer, baseline Kubernetes NetworkPolicies, and a default-deny verifier.

Source article: [Network Security Documentation Template](https://stackpractices.com/docs/network-security-template/)

## Files

- `network-security-inventory.md` — the blank inventory template, ready to copy into your runbook
- `sg_audit.py` — audits every security group rule and exports a CSV/JSON report with severity (`critical` for `0.0.0.0/0` inbound on non-web ports, `warning` otherwise)
- `flow_log_analysis.sh` — queries VPC flow logs for rejected traffic and ranks source IPs scanning your network
- `k8s-networkpolicies.yaml` — default-deny + DNS egress + frontend-to-backend NetworkPolicy baseline
- `check_default_deny.sh` — fails if any namespace lacks a default-deny NetworkPolicy

## How to use

1. Copy `network-security-inventory.md` and fill each section from live config — the article's "How to Fill Each Section" table maps every row to the CLI command that produces it.
2. Run `python sg_audit.py --region us-east-1` for a one-shot security group audit; attach the CSV to your review.
3. Run `./flow_log_analysis.sh /aws/vpc/flow-logs` to spot scanning attempts and lateral movement.
4. Apply `k8s-networkpolicies.yaml` per namespace, then verify coverage with `./check_default_deny.sh`.

## Requirements

- `sg_audit.py`: Python 3.9+, `boto3`, credentials with `ec2:DescribeSecurityGroups`
- `flow_log_analysis.sh`: AWS CLI, CloudWatch Logs read access, VPC flow logs enabled
- Kubernetes scripts: `kubectl`, `jq`, a CNI that enforces NetworkPolicy (Cilium, Calico)
