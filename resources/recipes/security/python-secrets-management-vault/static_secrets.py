"""Static KV v2 secret operations."""
from __future__ import annotations

import hvac


def store_secret(vault: hvac.Client, path: str, secret_data: dict) -> None:
    """Create or update a KV v2 secret at the given path."""
    vault.secrets.kv.v2.create_or_update_secret(
        path=path,
        secret=secret_data,
        mount_point="secret",
    )


def get_secret(vault: hvac.Client, path: str, version: int | None = None) -> dict:
    """Read a specific version (latest by default) of a KV v2 secret."""
    response = vault.secrets.kv.v2.read_secret_version(
        path=path,
        version=version,
        mount_point="secret",
    )
    return response["data"]["data"]


def list_secrets(vault: hvac.Client, path: str = "") -> list[str]:
    """List keys under a path. Returns [] when the path does not exist."""
    try:
        response = vault.secrets.kv.v2.list_secrets(
            path=path,
            mount_point="secret",
        )
        return response["data"]["keys"]
    except hvac.exceptions.InvalidPath:
        return []


if __name__ == "__main__":
    from vault_client import create_vault_client

    vault = create_vault_client()

    store_secret(vault, "myapp/database", {
        "username": "app_user",
        "password": "super-secret-password",
        "host": "db.example.com",
        "port": "5432",
    })

    store_secret(vault, "myapp/api_keys", {
        "stripe": "sk_live_xxx",
        "sendgrid": "SG.xxx",
    })

    db_creds = get_secret(vault, "myapp/database")
    print(f"DB Host: {db_creds['host']}")
    print(f"DB User: {db_creds['username']}")

    keys = list_secrets(vault, "myapp")
    print(f"Secrets under myapp/: {keys}")
