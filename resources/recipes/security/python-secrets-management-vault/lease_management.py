"""Lease renewal and revocation helpers."""
from __future__ import annotations

import time

import hvac


def renew_lease(vault: hvac.Client, lease_id: str, increment: int = 3600) -> bool:
    """Renew a lease. Returns False if the lease is no longer renewable."""
    try:
        vault.sys.renew_lease(
            lease_id=lease_id,
            increment=increment,
        )
        return True
    except hvac.exceptions.InvalidRequest:
        return False


def revoke_lease(vault: hvac.Client, lease_id: str) -> None:
    """Revoke a lease immediately, dropping the dynamic user."""
    vault.sys.revoke_lease(lease_id=lease_id)


if __name__ == "__main__":
    from vault_client import create_vault_client
    from dynamic_secrets import get_dynamic_db_credentials

    vault = create_vault_client()
    creds = get_dynamic_db_credentials(vault)

    # Wait until just before expiry, then renew
    time.sleep(max(0, creds["lease_duration"] - 300))
    renewed = renew_lease(vault, creds["lease_id"], increment=3600)
    print(f"Lease renewed: {renewed}")

    # Revoke when done
    revoke_lease(vault, creds["lease_id"])
    print("Lease revoked")
