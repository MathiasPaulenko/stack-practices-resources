#!/usr/bin/env bash
# Deploy an HTTP Cloud Function (Gen 2) with Express, Firestore and Secret Manager.
# Usage: GCP_PROJECT=my-project-id GCP_REGION=us-central1 ./deploy.sh
set -euo pipefail

PROJECT="${GCP_PROJECT:?Set GCP_PROJECT}"
REGION="${GCP_REGION:-us-central1}"
FUNCTION_NAME="${FUNCTION_NAME:-my-api}"

gcloud config set project "$PROJECT"

gcloud services enable \
  cloudfunctions.googleapis.com \
  cloudbuild.googleapis.com \
  run.googleapis.com \
  eventarc.googleapis.com \
  secretmanager.googleapis.com \
  firestore.googleapis.com \
  --project="$PROJECT"

gcloud functions deploy "$FUNCTION_NAME" \
  --gen2 \
  --runtime=nodejs20 \
  --region="$REGION" \
  --source=. \
  --entry-point=api \
  --trigger-http \
  --allow-unauthenticated \
  --memory=512MB \
  --timeout=60s \
  --concurrency=80 \
  --min-instances=0 \
  --max-instances=100 \
  --set-env-vars=NODE_ENV=production \
  --set-secrets=API_KEY=api-key:latest \
  --project="$PROJECT"

gcloud functions describe "$FUNCTION_NAME" \
  --gen2 --region="$REGION" --project="$PROJECT" \
  --format='value(serviceConfig.uri)'
