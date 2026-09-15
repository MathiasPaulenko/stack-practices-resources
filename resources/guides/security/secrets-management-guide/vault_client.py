"""HashiCorp Vault: read static secrets and generate on-demand DB credentials.

Usage:
    python vault_client.py

Prerequisites:
    pip install hvac
    VAULT_ADDR and VAULT_TOKEN environment variables set, or Kubernetes service account.
"""

import hvac


def read_static_secret(client: hvac.Client, path: str) -> dict:
    """Read a static secret from Vault KV v2."""
    secret = client.secrets.kv.v2.read_secret_version(path=path)
    return secret["data"]["data"]


def generate_db_credentials(client: hvac.Client, role: str) -> dict:
    """Generate on-demand database credentials."""
    creds = client.secrets.database.generate_credentials(name=role)
    return {
        "username": creds["data"]["username"],
        "password": creds["data"]["password"],
        "lease_id": creds["lease_id"],
        "lease_duration": creds["lease_duration"],
    }


if __name__ == "__main__":
    client = hvac.Client(url="https://vault.example.com")
    # For Kubernetes auth: client.auth.kubernetes.login(role='my-app', jwt=service_account_token)

    # Read a static secret
    config = read_static_secret(client, "my-app/config")
    print(f"API key: {config.get('api_key', 'NOT FOUND')}")

    # Generate on-demand DB credentials
    creds = generate_db_credentials(client, "app")
    print(f"DB user: {creds['username']}")
    print(f"DB password: {creds['password']}")
    print(f"Lease: {creds['lease_id']} (expires in {creds['lease_duration']}s)")
