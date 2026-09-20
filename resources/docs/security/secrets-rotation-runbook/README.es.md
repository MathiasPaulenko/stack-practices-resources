# Runbook de Rotación de Secretos — Recursos Companion

Archivos companion del [Runbook de Rotación de Secretos](https://stackpractices.com/es/docs/secrets-rotation-runbook/) en StackPractices.com.

## Qué incluye

| Archivo | Lenguaje | Descripción |
|---------|----------|-------------|
| `rotate_database_password.py` | Python | Rotación manual de contraseña de base de datos: generar → ALTER USER → actualizar secreto → verificar |
| `rotation_lambda.py` | Python | Lambda de rotación de AWS Secrets Manager con el contrato de 4 pasos (`createSecret`/`setSecret`/`testSecret`/`finishSecret`) |
| `vault-setup.sh` | Bash | Configuración del motor de secretos de base de datos de Vault: montaje, conexión, rotación de root, rol dinámico |
| `secret-inventory.csv` | CSV | Inventario de secretos listo para rellenar con tipo, responsable, ventana de rotación y fechas |

## Inicio rápido

### 1. Rotar una contraseña de base de datos manualmente

```bash
pip install boto3 psycopg2-binary
python rotate_database_password.py prod/payment-service/db-credentials
```

### 2. Desplegar la Lambda de rotación

Empaqueta `rotation_lambda.py` con una capa `psycopg2-binary` y asóciala:

```bash
aws secretsmanager rotate-secret \
  --secret-id prod/payment-service/db-credentials \
  --rotation-lambda-arn arn:aws:lambda:us-east-1:123456789012:function:secrets-rotation \
  --rotation-rules AutomaticallyAfterDays=90
```

### 3. Configurar credenciales dinámicas en Vault

```bash
export VAULT_ADDR="https://vault.example.com:8200"
export VAULT_DB_ADMIN_PASSWORD="<contraseña de admin>"
./vault-setup.sh
```

## Prerrequisitos

- Python 3.8+ con `boto3` y `psycopg2-binary`
- Credenciales de AWS con acceso a Secrets Manager y (para el script) a la base de datos
- CLI de Vault y un token con permisos de escritura en `database/*` para `vault-setup.sh`
- Una base de datos PostgreSQL para los ejemplos de rotación (adapta `ALTER USER` para MySQL)

## Referencias

- [AWS Secrets Manager — Rotación de secretos](https://docs.aws.amazon.com/secretsmanager/latest/userguide/rotating-secrets.html)
- [HashiCorp Vault — Motor de secretos de base de datos](https://developer.hashicorp.com/vault/docs/secrets/databases)
- [NIST SP 800-57 — Recomendaciones de gestión de claves](https://csrc.nist.gov/pubs/sp/800/57/pt1/r5/final)
