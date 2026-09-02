"""Transit engine for encryption without holding keys."""
from __future__ import annotations

import base64

import hvac


def create_key(vault: hvac.Client, key_name: str, key_type: str = "aes256-gcm96") -> None:
    """Create a named encryption key in the Transit engine."""
    vault.write(f"transit/keys/{key_name}", {"type": key_type})


def encrypt_data(vault: hvac.Client, key_name: str, plaintext: str) -> str:
    """Encrypt plaintext with the named Transit key. Returns ciphertext."""
    encoded = base64.b64encode(plaintext.encode()).decode()
    response = vault.write(f"transit/encrypt/{key_name}", {"plaintext": encoded})
    return response["data"]["ciphertext"]


def decrypt_data(vault: hvac.Client, key_name: str, ciphertext: str) -> str:
    """Decrypt ciphertext with the named Transit key. Returns plaintext."""
    response = vault.write(f"transit/decrypt/{key_name}", {"ciphertext": ciphertext})
    return base64.b64decode(response["data"]["plaintext"]).decode()


if __name__ == "__main__":
    from vault_client import create_vault_client

    vault = create_vault_client()
    vault.sys.enable_secrets_engine(backend_type="transit", path="transit")

    create_key(vault, "my-key")
    encrypted = encrypt_data(vault, "my-key", "sensitive data")
    print(f"Encrypted: {encrypted}")

    decrypted = decrypt_data(vault, "my-key", encrypted)
    print(f"Decrypted: {decrypted}")
