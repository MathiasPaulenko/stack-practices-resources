# Keep at least 2 containers warm to absorb cold starts
gcloud run deploy api-service \
  --image gcr.io/project/api:latest \
  --min-instances 2 \
  --max-instances 100 \
  --region us-central1
