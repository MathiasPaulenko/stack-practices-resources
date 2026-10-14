# Terraform Module Versioning Policy — Companion Files

Assets from the StackPractices template:
[Terraform Module Versioning Policy Template](https://stackpractices.com/docs/terraform-module-versioning-policy/)

## Files

| File | Purpose |
| --- | --- |
| `versions.tf` | Terraform + provider version constraints (raising the floor = breaking change) |
| `release.yml` | GitHub Actions release pipeline: tag → fmt/validate/tests → docs → GitHub Release |
| `validate.yml` | PR validation matrix across Terraform versions + tfsec + infracost |
| `CHANGELOG.md` | Keep a Changelog example with semver sections (Added/Changed/Deprecated/Breaking) |
| `MIGRATION-GUIDE.md` | Before/after migration guide for a breaking major release |
| `examples/basic/` | Minimal consumer with an exact version pin (production default) |

## Use

```bash
# Copy the workflows into your module repo
cp release.yml your-module/.github/workflows/
cp validate.yml your-module/.github/workflows/

# Copy the policy files into the module root
cp versions.tf CHANGELOG.md MIGRATION-GUIDE.md your-module/
```
