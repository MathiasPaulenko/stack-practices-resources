"""Thread-safe Vault secret manager with auto-renewal for dynamic credentials."""
from __future__ import annotations

import threading
import time

import hvac

from static_secrets import get_secret


class VaultSecretManager:
    """Wraps an hvac.Client with in-memory caching and lease auto-renewal."""

    def __init__(self, vault_client: hvac.Client):
        self.vault = vault_client
        self._dynamic_creds: dict[str, dict] = {}
        self._lock = threading.Lock()

    def get_static_secret(self, path: str) -> dict:
        return get_secret(self.vault, path)

    def get_dynamic_secret(self, role_path: str, name: str = "default") -> dict:
        with self._lock:
            if name in self._dynamic_creds:
                creds = self._dynamic_creds[name]
                if creds["expires_at"] - time.time() < 300:
                    self._renew(name)
                return creds

            response = self.vault.read(role_path)
            creds = {
                "username": response["data"]["username"],
                "password": response["data"]["password"],
                "lease_id": response["lease_id"],
                "lease_duration": response["lease_duration"],
                "expires_at": time.time() + response["lease_duration"],
            }
            self._dynamic_creds[name] = creds
            return creds

    def _renew(self, name: str) -> None:
        creds = self._dynamic_creds[name]
        try:
            self.vault.sys.renew_lease(
                lease_id=creds["lease_id"],
                increment=creds["lease_duration"],
            )
            creds["expires_at"] = time.time() + creds["lease_duration"]
        except hvac.exceptions.InvalidRequest:
            del self._dynamic_creds[name]

    def cleanup(self) -> None:
        with self._lock:
            for creds in self._dynamic_creds.values():
                try:
                    self.vault.sys.revoke_lease(creds["lease_id"])
                except Exception:
                    pass
            self._dynamic_creds.clear()


if __name__ == "__main__":
    from vault_client import create_vault_client

    vault = create_vault_client()
    manager = VaultSecretManager(vault)

    db_creds = manager.get_dynamic_secret("database/creds/app-role", "main_db")
    print(f"Using DB user: {db_creds['username']}")

    manager.cleanup()
    print("All leases revoked")
