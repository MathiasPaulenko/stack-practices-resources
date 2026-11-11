# GCP Cloud Functions with Node.js — Companion Resources

Runnable companion for the recipe [Deploy HTTP Cloud Functions on Google Cloud with Node.js](https://stackpractices.com/recipes/gcp-cloud-functions-nodejs/) ([versión en español](https://stackpractices.com/es/recipes/gcp-cloud-functions-nodejs/)).

## Contents

| File | Purpose |
| --- | --- |
| `index.js` | Express API registered as a Gen 2 HTTP function: Firestore CRUD, Secret Manager caching, CORS, central error handler |
| `scheduled.js` | HTTP handler invoked by Cloud Scheduler (OIDC) — the correct alternative to a `--schedule` flag that doesn't exist |
| `deploy.sh` | `gcloud` script: enables APIs and deploys `my-api` (Gen 2, nodejs20, concurrency, secrets) |
| `deploy-scheduled.sh` | Deploys a private function, grants `run.invoker` to the scheduler service account, creates the cron job |
| `package.json` | Dependencies and `npm start` for local runs via the Functions Framework |

## Run locally

```bash
npm install
npm start                      # serves on http://localhost:8080
curl http://localhost:8080/health
```

## Deploy

```bash
export GCP_PROJECT=my-project-id
./deploy.sh                    # public HTTP API
./deploy-scheduled.sh          # private function + Cloud Scheduler job
```

The scheduled path needs a service account (`scheduler-sa@<project>.iam.gserviceaccount.com`) and the Cloud Scheduler API enabled.

## License

MIT — companion files for educational use.
