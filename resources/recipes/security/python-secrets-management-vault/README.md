# Python Secrets Management with HashiCorp Vault

Companion code for the StackPractices recipe
[Manage Application Secrets with HashiCorp Vault and Python](https://stackpractices.com/recipes/python-secrets-management-vault/).

## Requirements

- Python 3.11+
- [HashiCorp Vault CLI](https://developer.hashicorp.com/vault/install) (for the dev server used in tests)
- Docker (optional, for the `docker-compose.yml` dev server)

## Setup

```bash
pip install -r requirements.txt
```

## Run the dev Vault server

Option A — local CLI:

```bash
vault server -dev -dev-root-token-id=root
export VAULT_ADDR=http://127.0.0.1:8200
export VAULT_TOKEN=root
```

Option B — Docker Compose:

```bash
docker compose up -d
export VAULT_ADDR=http://127.0.0.1:8200
export VAULT_TOKEN=root
```

## Files

| File | Purpose |
| --- | --- |
| `vault_client.py` | Connection helper |
| `static_secrets.py` | KV v2 store, read, list |
| `dynamic_secrets.py` | Database secrets engine setup and credential generation |
| `lease_management.py` | Lease renewal and revocation |
| `vault_secret_manager.py` | Thread-safe wrapper with auto-renewal |
| `approle_auth.py` | AppRole authentication |
| `transit_encrypt.py` | Transit engine encrypt/decrypt |
| `kubernetes_auth.py` | Kubernetes authentication from a pod |
| `test_vault.py` | pytest suite (requires the dev server) |

## Run the tests

```bash
pytest test_vault.py -v
```

## Run the examples

```bash
python vault_client.py
python static_secrets.py
python dynamic_secrets.py
python transit_encrypt.py
```

## Production notes

- Never use the `root` token in production. Use AppRole or Kubernetes auth.
- Enable audit logging (`vault audit enable file file_path=/var/log/vault/audit.log`).
- Use mTLS between the application and Vault.
- Cache secrets locally with a short TTL to survive Vault outages.
