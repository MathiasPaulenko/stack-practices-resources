# Secrets Management Guide — Companion Resources

Companion files for the [Secrets Management Guide](https://stackpractices.com/guides/secrets-management-guide/) on StackPractices.com.

## What's included

| File | Language | Description |
|------|----------|-------------|
| `vault_client.py` | Python | HashiCorp Vault: read static secrets, generate on-demand DB credentials |
| `aws_secrets_manager.py` | Python | AWS Secrets Manager: create, retrieve, and rotate secrets |
| `azure_key_vault.py` | Python | Azure Key Vault: retrieve secrets using Managed Identity |
| `scan_secrets.sh` | Bash | Secret scanning with TruffleHog, Gitleaks, and detect-secrets |
| `external-secret.yaml` | YAML | External Secrets Operator: sync AWS secrets to Kubernetes |

## Quick start

### Vault (Python)

```bash
pip install hvac
export VAULT_ADDR=https://vault.example.com
export VAULT_TOKEN=your-token
python vault_client.py
```

### AWS Secrets Manager (Python)

```bash
pip install boto3
aws configure
python aws_secrets_manager.py
```

### Azure Key Vault (Python)

```bash
pip install azure-identity azure-keyvault-secrets
python azure_key_vault.py
```

### Secret scanning

```bash
chmod +x scan_secrets.sh
./scan_secrets.sh .
```

### External Secrets Operator (Kubernetes)

```bash
kubectl apply -f external-secret.yaml
```

## References

- [HashiCorp Vault documentation](https://developer.hashicorp.com/vault/docs)
- [AWS Secrets Manager documentation](https://docs.aws.amazon.com/secretsmanager/latest/userguide/intro.html)
- [OWASP Secrets Management Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Secrets_Management_Cheat_Sheet.html)
