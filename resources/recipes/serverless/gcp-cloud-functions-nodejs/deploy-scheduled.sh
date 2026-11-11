#!/usr/bin/env bash
# Deploy a privately-invoked Cloud Function and wire a Cloud Scheduler cron job to it.
# There is no --schedule flag on `gcloud functions deploy`; scheduling lives in Scheduler.
# Usage: GCP_PROJECT=my-project-id SCHEDULER_SA=scheduler-sa ./deploy-scheduled.sh
set -euo pipefail

PROJECT="${GCP_PROJECT:?Set GCP_PROJECT}"
REGION="${GCP_REGION:-us-central1}"
SA="${SCHEDULER_SA:-scheduler-sa}"
FUNCTION_NAME="${FUNCTION_NAME:-scheduled-cleanup}"
JOB_NAME="${JOB_NAME:-scheduled-cleanup-job}"
CRON="${CRON:-0 2 * * *}"

gcloud config set project "$PROJECT"

gcloud functions deploy "$FUNCTION_NAME" \
  --gen2 \
  --runtime=nodejs20 \
  --region="$REGION" \
  --source=. \
  --entry-point=scheduledCleanup \
  --trigger-http \
  --no-allow-unauthenticated \
  --project="$PROJECT"

gcloud functions add-invoker-policy-binding "$FUNCTION_NAME" \
  --gen2 \
  --region="$REGION" \
  --member="serviceAccount:${SA}@${PROJECT}.iam.gserviceaccount.com" \
  --project="$PROJECT"

URI="$(gcloud functions describe "$FUNCTION_NAME" \
  --gen2 --region="$REGION" --project="$PROJECT" \
  --format='value(serviceConfig.uri)')"

gcloud scheduler jobs create http "$JOB_NAME" \
  --location="$REGION" \
  --schedule="$CRON" \
  --uri="$URI" \
  --http-method=POST \
  --oidc-service-account-email="${SA}@${PROJECT}.iam.gserviceaccount.com" \
  --time-zone="UTC" \
  --project="$PROJECT"

echo "Scheduler job $JOB_NAME -> $URI"
