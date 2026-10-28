# Blob Storage: S3, GCS, and Azure Blob Patterns

Companion code for the [Blob Storage guide](https://stackpractices.com/guides/blob-storage-guide/) on StackPractices.

## Files

| File | What it does |
|---|---|
| `s3_upload.py` | Presigned PUT/GET URLs plus automatic multipart upload via boto3 TransferConfig |
| `lifecycle.json` | S3 lifecycle rule: Standard → IA (30d) → Glacier (90d) → Deep Archive (1y), expired aborts at 7d |
| `cors.json` | Bucket CORS rule scoped to your origin for direct browser uploads |

## Usage

```bash
# Generate a presigned upload URL and push a file
python s3_upload.py --bucket myapp-uploads-prod --key uploads/2025/10/report.pdf \
  --file report.pdf --type application/pdf

# Apply the lifecycle rule
aws s3api put-bucket-lifecycle-configuration \
  --bucket myapp-reports-prod \
  --lifecycle-configuration file://lifecycle.json

# Apply CORS for browser uploads
aws s3api put-bucket-cors \
  --bucket myapp-uploads-prod \
  --cors-configuration file://cors.json
```

Azure's equivalent uses `generate_blob_sas` for SAS tokens and `BlobClient.upload_blob(max_concurrency=N)` for automatic chunking — see the guide's Step 2 and Step 3 for working code.
