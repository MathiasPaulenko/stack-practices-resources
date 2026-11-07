# policies/checks.tf — native `check` blocks (Terraform >= 1.5). The OSS
# alternative to Sentinel/OPA: they run in every plan/apply.
# Assumes a resource `aws_s3_bucket_public_access_block.app` exists in the
# configuration that manages this bucket.

check "s3_no_public_access" {
  assert {
    condition = aws_s3_bucket_public_access_block.app.block_public_acls &&
                aws_s3_bucket_public_access_block.app.block_public_policy &&
                aws_s3_bucket_public_access_block.app.ignore_public_acls &&
                aws_s3_bucket_public_access_block.app.restrict_public_buckets
    error_message = "S3 bucket must block all public access."
  }
}
