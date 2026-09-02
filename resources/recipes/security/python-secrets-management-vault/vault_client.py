"""Vault client connection helper."""
from __future__ import annotations

import os

import hvac


def create_vault_client() -> hvac.Client:
    """Create and authenticate an hvac.Client.

    Reads VAULT_ADDR (default http://127.0.0.1:8200) and VAULT_TOKEN
    (default root, dev mode only) from the environment.
    """
    client = hvac.Client(
        url=os.getenv("VAULT_ADDR", "http://127.0.0.1:8200"),
        token=os.getenv("VAULT_TOKEN", "root"),
    )

    if not client.is_authenticated():
        raise RuntimeError("Vault authentication failed")

    return client


if __name__ == "__main__":
    vault = create_vault_client()
    print(f"Connected to Vault at {vault.url}")
