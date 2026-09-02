"""Kubernetes authentication for Vault from inside a pod."""
from __future__ import annotations

import hvac


def authenticate_kubernetes(
    vault: hvac.Client,
    role: str,
    jwt_path: str = "/var/run/secrets/kubernetes.io/serviceaccount/token",
) -> str:
    """Read the pod's service account JWT and exchange it for a Vault token."""
    with open(jwt_path) as f:
        jwt_token = f.read()

    response = vault.auth.kubernetes.login(
        role=role,
        jwt=jwt_token,
    )
    return response["auth"]["client_token"]


def build_client_from_kubernetes(
    url: str,
    role: str,
    jwt_path: str = "/var/run/secrets/kubernetes.io/serviceaccount/token",
) -> hvac.Client:
    """Authenticate via Kubernetes and return a ready-to-use hvac.Client."""
    bootstrap = hvac.Client(url=url)
    token = authenticate_kubernetes(bootstrap, role, jwt_path)
    return hvac.Client(url=url, token=token)


if __name__ == "__main__":
    import os

    client = build_client_from_kubernetes(
        url=os.getenv("VAULT_ADDR", "http://127.0.0.1:8200"),
        role="my-app-role",
    )
    print(f"Authenticated via Kubernetes: {client.is_authenticated()}")
