"""AppRole authentication for machine-to-machine Vault access."""
from __future__ import annotations

import hvac


def authenticate_approle(
    vault: hvac.Client,
    role_id: str,
    secret_id: str,
) -> str:
    """Login with AppRole credentials and return a client token."""
    response = vault.auth.approle.login(
        role_id=role_id,
        secret_id=secret_id,
    )
    return response["auth"]["client_token"]


def build_client_from_approle(
    url: str,
    role_id: str,
    secret_id: str,
) -> hvac.Client:
    """Authenticate with AppRole and return a ready-to-use hvac.Client."""
    bootstrap = hvac.Client(url=url)
    token = authenticate_approle(bootstrap, role_id, secret_id)
    return hvac.Client(url=url, token=token)


if __name__ == "__main__":
    import os

    client = build_client_from_approle(
        url=os.getenv("VAULT_ADDR", "http://127.0.0.1:8200"),
        role_id="role-uuid",
        secret_id="secret-uuid",
    )
    print(f"Authenticated via AppRole: {client.is_authenticated()}")
