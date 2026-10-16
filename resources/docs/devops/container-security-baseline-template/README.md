# Container Security Baseline Template — Companion Code

Downloadable manifests for the [Container Security Baseline Template](https://stackpractices.com/docs/container-security-baseline-template/) on StackPractices.

## Contents

| Path | What it contains |
|------|------------------|
| `policies/kyverno-enforce-non-root.yaml` | ClusterPolicy requiring `runAsNonRoot` and `runAsUser` above 10000 |
| `policies/kyverno-disallow-privileged.yaml` | ClusterPolicy rejecting privileged containers using the `=()` conditional anchor |
| `policies/kyverno-require-resources.yaml` | ClusterPolicy requiring CPU/memory requests and limits |
| `policies/namespace-pod-security.yaml` | Namespace labels enforcing `baseline` while warning at `restricted` |
| `network/default-deny-all.yaml` | NetworkPolicy denying all ingress and egress in a namespace |
| `network/allow-frontend-to-backend.yaml` | Explicit ingress allow rule between two workloads |
| `network/allow-dns-egress.yaml` | Egress rule allowing DNS to kube-dns |
| `secrets/external-secret-registry.yaml` | ExternalSecret syncing registry credentials from a vault |
| `exceptions/exception-register.md` | Exception and risk-acceptance register template |

## Usage

1. Review each file and adjust namespaces, labels, ports, and version pins to your environment.
2. Apply policies in `Audit`/`warn` mode first; switch to `Enforce` after fixing violations.
3. Keep the exception register in a shared location and review it quarterly.

See the template page for the rollout sequence, verification steps, and the reasoning behind each control.
