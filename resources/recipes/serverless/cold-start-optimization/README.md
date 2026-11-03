# Cold Start Optimization — Companion Files

Companion to the StackPractices recipe [Cold Start Optimization: AWS Lambda, Azure, Cloud Run](https://stackpractices.com/recipes/cold-start-optimization/).

| File | Contains |
|---|---|
| src/provisioned-concurrency.tf | Terraform for Lambda provisioned concurrency on a published version |
| src/OrderHandler.java | SnapStart-ready Java handler with init-time snapshot |
| src/azure-premium-deploy.sh | Azure Functions Premium plan deploy with pre-warmed instances |
| src/deploy-cloudrun.sh | Cloud Run deploy with `--min-instances` warm pool |
| src/lazy-init.py | Python lazy-initialization pattern for heavy resources |

## Usage

- Copy `provisioned-concurrency.tf` into your infra and adjust `function_name`/`memory_size`; remember `publish = true` is required.
- `OrderHandler.java` shows where SnapStart snapshots init — keep stateful resources out of the snapshot.
- Run the two shell scripts as templates for Azure Premium and Cloud Run deployments.
- `lazy-init.py` shows module-level vs lazy init placement for clients.
