# Gestión de Secretos en Python con HashiCorp Vault

Código companion de la receta de StackPractices
[Gestiona Secretos de Aplicación con HashiCorp Vault y Python](https://stackpractices.com/es/recipes/python-secrets-management-vault/).

## Requisitos

- Python 3.11+
- [HashiCorp Vault CLI](https://developer.hashicorp.com/vault/install) (para el dev server usado en tests)
- Docker (opcional, para el dev server con `docker-compose.yml`)

## Instalación

```bash
pip install -r requirements.txt
```

## Levantar el dev server de Vault

Opción A — CLI local:

```bash
vault server -dev -dev-root-token-id=root
export VAULT_ADDR=http://127.0.0.1:8200
export VAULT_TOKEN=root
```

Opción B — Docker Compose:

```bash
docker compose up -d
export VAULT_ADDR=http://127.0.0.1:8200
export VAULT_TOKEN=root
```

## Archivos

| Archivo | Propósito |
| --- | --- |
| `vault_client.py` | Helper de conexión |
| `static_secrets.py` | KV v2: guardar, leer, listar |
| `dynamic_secrets.py` | Configuración del database secrets engine y generación de credenciales |
| `lease_management.py` | Renovación y revocación de leases |
| `vault_secret_manager.py` | Wrapper thread-safe con auto-renovación |
| `approle_auth.py` | Autenticación AppRole |
| `transit_encrypt.py` | Encriptación con motor Transit |
| `kubernetes_auth.py` | Autenticación Kubernetes desde un pod |
| `test_vault.py` | Suite de pytest (requiere el dev server) |

## Ejecutar los tests

```bash
pytest test_vault.py -v
```

## Ejecutar los ejemplos

```bash
python vault_client.py
python static_secrets.py
python dynamic_secrets.py
python transit_encrypt.py
```

## Notas de producción

- Nunca uses el token `root` en producción. Usá AppRole o Kubernetes auth.
- Habilitá audit logging (`vault audit enable file file_path=/var/log/vault/audit.log`).
- Usá mTLS entre la aplicación y Vault.
- Cacheá secretos localmente con un TTL corto para sobrevivir a cortes de Vault.
