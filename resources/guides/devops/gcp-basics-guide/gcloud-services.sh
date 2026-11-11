#!/usr/bin/env bash
# Service commands from the GCP Basics guide: GCE, GKE, Cloud Run, Storage, Cloud SQL
set -euo pipefail

# --- Compute Engine ---
gcloud compute instances create my-vm \
  --zone=us-central1-a \
  --machine-type=e2-medium \
  --image-family=ubuntu-2204-lts \
  --image-project=ubuntu-os-cloud \
  --boot-disk-size=20GB

# --- Google Kubernetes Engine (Standard) ---
gcloud container clusters create my-cluster \
  --zone=us-central1-a \
  --num-nodes=3 \
  --enable-autoscaling \
  --min-nodes=1 \
  --max-nodes=10

kubectl create deployment hello-app --image=gcr.io/project/hello-app:v1
kubectl expose deployment hello-app --type=LoadBalancer --port=80

# --- Cloud Run ---
gcloud run deploy hello-service \
  --image=gcr.io/project/hello-app:v1 \
  --platform=managed \
  --region=us-central1 \
  --allow-unauthenticated

# --- Cloud Storage (use `gcloud storage`, not legacy `gsutil`) ---
gcloud storage buckets create gs://my-app-bucket --location=us-central1
gcloud storage cp app.zip gs://my-app-bucket/builds/
gcloud storage rsync ./dist gs://my-app-bucket/static --recursive

# --- Persistent Disk ---
gcloud compute disks create my-disk --size=100GB --type=pd-ssd --zone=us-central1-a
gcloud compute instances attach-disk my-vm --disk=my-disk --zone=us-central1-a

# --- Cloud SQL (PostgreSQL, dev tier) ---
gcloud sql instances create mydb \
  --database-version=POSTGRES_15 \
  --tier=db-f1-micro \
  --region=us-central1 \
  --storage-size=10GB

gcloud sql databases create myapp --instance=mydb
