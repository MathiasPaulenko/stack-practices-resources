# Guía de Gestión de Secretos — Recursos Companion

Archivos companion de la [Guía de Gestión de Secretos](https://stackpractices.com/es/guides/secrets-management-guide/) en StackPractices.com.

## Qué incluye

| Archivo | Lenguaje | Descripción |
|---------|----------|-------------|
| `vault_client.py` | Python | HashiCorp Vault: leer secretos estáticos, generar credenciales de DB bajo demanda |
| `aws_secrets_manager.py` | Python | AWS Secrets Manager: crear, recuperar y rotar secretos |
| `azure_key_vault.py` | Python | Azure Key Vault: recuperar secretos usando Managed Identity |
| `scan_secrets.sh` | Bash | Escaneo de secretos con TruffleHog, Gitleaks y detect-secrets |
| `external-secret.yaml` | YAML | External Secrets Operator: sincronizar secretos de AWS a Kubernetes |

## Inicio rápido

### Vault (Python)

```bash
pip install hvac
export VAULT_ADDR=https://vault.example.com
export VAULT_TOKEN=tu-token
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

### Escaneo de secretos

```bash
chmod +x scan_secrets.sh
./scan_secrets.sh .
```

### External Secrets Operator (Kubernetes)

```bash
kubectl apply -f external-secret.yaml
```

## Referencias

- [Documentación de HashiCorp Vault](https://developer.hashicorp.com/vault/docs)
- [Documentación de AWS Secrets Manager](https://docs.aws.amazon.com/secretsmanager/latest/userguide/intro.html)
- [Cheat Sheet de Gestión de Secretos de OWASP](https://cheatsheetseries.owasp.org/cheatsheets/Secrets_Management_Cheat_Sheet.html)
