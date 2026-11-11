#!/usr/bin/env bash
# Account, project, API and billing setup from the GCP Basics guide
set -euo pipefail

# Interactive auth + default project/region
gcloud init

# Application Default Credentials for local SDK code — separate from `gcloud init`
gcloud auth application-default login

# Set the working project explicitly (most "wrong project" mistakes start here)
gcloud config set project my-project

# Enable the APIs a typical web workload needs — nothing works until these are on
gcloud services enable compute.googleapis.com \
  run.googleapis.com sqladmin.googleapis.com \
  storage.googleapis.com bigquery.googleapis.com

# Budget with alerts — notifies, never caps. Replace with your billing account ID
# (find it with: gcloud billing accounts list)
gcloud billing budgets create \
  --billing-account=XXXXXX-XXXXXX-XXXXXX \
  --display-name="Dev budget" \
  --budget-amount=50USD \
  --threshold-rule=percent=50 \
  --threshold-rule=percent=90 \
  --threshold-rule=percent=100
