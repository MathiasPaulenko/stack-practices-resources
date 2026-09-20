# Secrets Rotation Runbook — Companion Resources

Companion files for the [Secrets Rotation Runbook](https://stackpractices.com/docs/secrets-rotation-runbook/) on StackPractices.com.

## What's included

| File | Language | Description |
|------|----------|-------------|
| `rotate_database_password.py` | Python | Standalone database password rotation: generate → ALTER USER → update secret → verify |
| `rotation_lambda.py` | Python | AWS Secrets Manager rotation Lambda implementing the 4-step contract (`createSecret`/`setSecret`/`testSecret`/`finishSecret`) |
| `vault-setup.sh` | Bash | Vault database secrets engine setup: mount, connection config, root rotation, dynamic role |
| `secret-inventory.csv` | CSV | Ready-to-fill secret inventory with type, owner, rotation window and due dates |

## Quick start

### 1. Rotate a database password manually

```bash
pip install boto3 psycopg2-binary
python rotate_database_password.py prod/payment-service/db-credentials
```

### 2. Deploy the rotation Lambda

Package `rotation_lambda.py` with a `psycopg2-binary` layer, then attach it:

```bash
aws secretsmanager rotate-secret \
  --secret-id prod/payment-service/db-credentials \
  --rotation-lambda-arn arn:aws:lambda:us-east-1:123456789012:function:secrets-rotation \
  --rotation-rules AutomaticallyAfterDays=90
```

### 3. Configure Vault dynamic credentials

```bash
export VAULT_ADDR="https://vault.example.com:8200"
export VAULT_DB_ADMIN_PASSWORD="<admin password>"
./vault-setup.sh
```

## Prerequisites

- Python 3.8+ with `boto3` and `psycopg2-binary`
- AWS credentials with Secrets Manager and (for the script) database access
- Vault CLI and a token with `database/*` write permissions for `vault-setup.sh`
- A PostgreSQL database for the rotation examples (adapt `ALTER USER` for MySQL)

## References

- [AWS Secrets Manager — Rotate secrets](https://docs.aws.amazon.com/secretsmanager/latest/userguide/rotating-secrets.html)
- [HashiCorp Vault — Database secrets engine](https://developer.hashicorp.com/vault/docs/secrets/databases)
- [NIST SP 800-57 — Key management recommendations](https://csrc.nist.gov/pubs/sp/800/57/pt1/r5/final)
