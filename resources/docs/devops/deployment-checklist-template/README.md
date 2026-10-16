# Deployment Checklist Template — Companion Resources

Downloadable files for the [Deployment Checklist Template](https://stackpractices.com/docs/deployment-checklist-template/) on StackPractices.

## Files

| File | What it is |
|------|------------|
| `deployment-checklist-template.md` | Blank markdown checklist covering pre-deployment, deployment, and post-deployment. Copy it into your wiki or repo and fill it per release. |
| `example-filled.md` | The same checklist filled in for a worked release (`api-billing v2.4.0` with a schema migration and a feature flag). |
| `canary-deploy.sh` | Canary deploy script for Kubernetes + Istio VirtualService. Requires `BUILD_TAG`; rolls back automatically if the canary error rate crosses 1%. |
| `deployment-communication.txt` | Plain-text template for narrating a deploy in your team's channel, with timestamps and a rollback reference. |

## Usage

1. Copy `deployment-checklist-template.md` into your repo or wiki.
2. Fill the metadata table and check items per release; delete sections that don't apply (e.g., Database for stateless changes).
3. Adapt `canary-deploy.sh` to your service name, namespace, and traffic tool (swap `virtualservice` for your ingress canary annotations if you don't run Istio).
4. Keep `deployment-communication.txt` open during the deploy and post updates as each step completes.
