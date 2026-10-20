# RBAC Policy Template — Companion Resources

Downloadable artifacts for the [RBAC Policy Template](https://stackpractices.com/docs/rbac-policy-template/) doc on StackPractices.

## Files

| File | What it is |
|------|------------|
| `rbac-policy-template.md` | The complete policy document template — role matrix, assignment rules, separation of duties, request workflow, review cadence, offboarding, break-glass, and exceptions. Fill in the bracketed placeholders. |
| `kubernetes-rbac.yaml` | Kubernetes `Role` + `RoleBinding` (read-only developers) and a `ClusterRole` for the platform team that manages RBAC objects. Apply with `kubectl apply -f kubernetes-rbac.yaml`. |
| `aws-iam-boundary-policy.json` | AWS IAM policy with least-privilege S3 access, a hard deny on bucket deletion, and an MFA requirement for sensitive IAM actions. |
| `opa-prevent-privilege-escalation.yaml` | OPA Gatekeeper constraint that blocks bindings to `cluster-admin` outside the platform and security teams. |
| `opa-rolebinding-validation.rego` | The Rego rule behind the constraint — validates role bindings against a forbidden-role list. |

## How to use

1. Copy `rbac-policy-template.md` into your policy repository and replace the bracketed placeholders.
2. Map each role row to a group in your identity provider or a binding in Kubernetes/cloud IAM.
3. Adapt the manifest and policy files to your namespaces, groups, and bucket names.
4. Store everything under version control — policy changes go through the same review as code.

## Related

- Doc: https://stackpractices.com/docs/rbac-policy-template/
- Recipe: https://stackpractices.com/recipes/implement-rbac/
- Doc (ES): https://stackpractices.com/es/docs/rbac-policy-template/
