# Network Segmentation Policy Template — Companion Resources

Downloadable files for the [Network Segmentation Policy Template](https://stackpractices.com/docs/network-segmentation-policy-template/) on StackPractices.

## Files

| File | What it is |
|------|------------|
| `network-segmentation-policy.md` | Blank fillable policy: zones, traffic matrix, controls, exceptions, roles. Copy into your wiki or repo. |
| `reachability-validator.py` | AWS SSM-based reachability tester that verifies zone isolation actually holds (allow/deny probes between subnets). |
| `calico-network-policies.yaml` | Two manifests: a stock Kubernetes `NetworkPolicy` default-deny plus a Calico `projectcalico.org/v3` workload-level allow. |
| `segmentation-module.tf` | Terraform module that creates a security group whose ingress/egress rules come entirely from variables — your traffic matrix as code. |

## Usage

1. Fill `network-segmentation-policy.md` starting with the traffic matrix (derive rows from real flow logs, not guesswork).
2. Apply `calico-network-policies.yaml` in staged/log mode before enforcing.
3. Adapt `segmentation-module.tf` to your CIDR plan; keep the allow-lists in `allowed_ingress`/`allowed_egress` aligned with the matrix.
4. Run `reachability-validator.py` from an authorized instance to confirm denies hold — especially after rule changes.
