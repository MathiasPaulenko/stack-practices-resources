# Compliance Gap Analysis Template — Companion Resources

Companion files for the [Compliance Gap Analysis Template](https://stackpractices.com/docs/compliance-gap-analysis-template/) on StackPractices.

## Contents

| File | Purpose |
|------|---------|
| `gap-analysis-template.csv` | Control mapping table as CSV — import into Sheets/Excel/Airtable and fill in your own rows |
| `remediation-plan.csv` | Remediation plan table as CSV, with priority, owner, due date, and evidence-needed columns |
| `collect-evidence.sh` | Collects AWS evidence for common SOC 2 controls (IAM MFA, S3 encryption, CloudTrail, AWS Config) into a dated evidence folder |
| `generate-mapping.py` | Generates a multi-framework mapping matrix (SOC 2 / ISO 27001 / PCI-DSS) from a single control inventory |

## Usage

```bash
# Fill in the CSVs in your spreadsheet tool, or
python -c "import csv; print(list(csv.reader(open('gap-analysis-template.csv')))[:2])"

# Collect AWS evidence (needs aws CLI with read-only creds)
aws sts get-caller-identity
./collect-evidence.sh

# Generate the multi-framework matrix
python generate-mapping.py
```

The CSVs match the tables in the doc: control mapping, gap summary, remediation plan, and evidence tracking. Extend `FRAMEWORK_MAPPING` in the Python script with your own controls to cover more requirement IDs.
