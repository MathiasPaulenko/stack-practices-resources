# Access Control Review Template — Companion Resources

Companion files for the [Access Control Review Template](https://stackpractices.com/docs/access-control-review-template/) on StackPractices.

## Contents

| File | Purpose |
|------|---------|
| `aws-iam-access-analyzer.sh` | Lists IAM users with last activity, flags unused access keys, and exports active IAM Access Analyzer findings (set `ANALYZER_ARN` to enable) |
| `github-org-access-audit.py` | Lists GitHub org members and flags accounts inactive beyond a 90-day threshold via the public events API |
| `k8s-rbac-audit.sh` | Audits cluster-admin bindings, per-namespace RoleBindings, and service accounts still carrying secret references |

## Usage

```bash
# AWS IAM snapshot
aws sts get-caller-identity   # verify credentials first
./aws-iam-access-analyzer.sh

# GitHub org audit
pip install requests
python github-org-access-audit.py <github-token>

# Kubernetes RBAC audit
kubectl config current-context  # verify context first
./k8s-rbac-audit.sh
```

Feed the output of these scripts into the access register in the review template — each finding becomes a row with a verdict (keep / modify / remove) and a reason.
