# GCP Basics Guide — Companion Resources

Runnable assets for the [GCP Basics guide](https://stackpractices.com/guides/gcp-basics-guide/) on StackPractices.

## Files

| File | Description |
|------|-------------|
| `gcloud-setup.sh` | First-day setup: `gcloud init`, ADC login, project config, API enablement, budget alerts |
| `gcloud-services.sh` | Service commands from the guide: GCE VM, GKE cluster, Cloud Run deploy, Cloud Storage, Persistent Disk, Cloud SQL |
| `bigquery_names.sql` | BigQuery query against a public dataset (top US baby names) |
| `iam-policy.yaml` | Least-privilege IAM bindings for a workload service account |
| `firestore_example.js` | Minimal Firestore write with the modular Firebase SDK |

## Usage

1. Install the gcloud CLI and run `gcloud init` first, then `gcloud auth application-default login` for local SDK code.
2. Replace placeholders (`my-project`, `my-app-bucket`, billing account ID) with your own values before running anything.
3. Billing budget alerts notify you — they never stop spending. Check Billing → Budgets & alerts in the console too.
