# Content Delivery Network (CDN) Pattern — Companion Code

Runnable snippets from the
[Content Delivery Network (CDN) Pattern](https://stackpractices.com/patterns/content-delivery-network-pattern/)
on StackPractices. Three moving parts of a CDN deployment: the distribution, the
cache-control headers, and the invalidation path.

## Files

| File | Description |
|------|-------------|
| `invalidate_cache.mjs` | AWS SDK v3 CloudFront invalidation — call from your deploy pipeline to purge paths or wildcards |
| `cdn_manager.py` | `CDNManager` with parallel cache warmup, purge, and HIT/MISS status checks (`X-Cache`, `Age` headers) |
| `cloudfront.tf` | Terraform CloudFront distribution — S3 + ALB origins, three cache behaviors, TLS 1.2, compression |
| `cache-control-headers.http` | `Cache-Control` recipes per content type: fingerprinted assets, HTML, personalized, APIs |

## Requirements

- `invalidate_cache.mjs`: Node 18+ and `@aws-sdk/client-cloudfront`
- `cdn_manager.py`: Python 3.10+ and `requests`
- `cloudfront.tf`: Terraform 1.x with the AWS provider and the referenced resources (`aws_s3_bucket.assets`, `aws_lb.main`, `aws_acm_certificate.cdn`, `aws_cloudfront_origin_access_identity.oai`)

## Usage

```bash
# Purge paths after a deploy
node invalidate_cache.mjs

# Warm up edge caches and check HIT/MISS
python cdn_manager.py

# Plan the distribution
terraform plan
```
