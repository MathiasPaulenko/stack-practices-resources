# Cloud Resource Tagging Policy — Runnable Tools

Companion to the StackPractices doc [Cloud Resource Tagging Policy Template](https://stackpractices.com/docs/cloud-resource-tagging-policy-template/).

## Files

| File | Stack | Purpose |
| --- | --- | --- |
| `src/detect-untagged.py` | Python 3.9+ + `boto3` | Scans EC2, S3 and RDS across regions for missing required tags (`team`, `environment`, `product`, `cost-center`, `owner`) and prints a JSON report. Handles the `NoSuchTagSet` error that untagged buckets raise. |
| `src/tag-policy.tf` | Terraform (AWS provider) | `required_tags` variable + `default_tags` local that applies the lowercase-hyphen convention to EC2, S3 and RDS resources. |

## Run

`src/detect-untagged.py` needs AWS credentials (env vars, `~/.aws` or instance profile) — it makes read-only `Describe`/`List` calls:

```bash
pip install boto3
python src/detect-untagged.py
```

`src/tag-policy.tf` is a module fragment, not a standalone project — copy the `locals`/`variable` block into your own Terraform and reference `local.default_tags` on taggable resources. Edit `REGIONS` in the script and the tag set in the `required_tags` map to match your policy.
