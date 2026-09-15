"""Azure Key Vault: store and retrieve secrets using Managed Identity.

Usage:
    python azure_key_vault.py

Prerequisites:
    pip install azure-identity azure-keyvault-secrets
    Azure Managed Identity assigned to the compute resource.
"""

from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient


def get_secret(vault_url: str, secret_name: str) -> str:
    """Retrieve a secret from Azure Key Vault using Managed Identity."""
    credential = DefaultAzureCredential()
    client = SecretClient(vault_url=vault_url, credential=credential)
    secret = client.get_secret(secret_name)
    return secret.value


if __name__ == "__main__":
    vault_url = "https://myvault.vault.azure.net/"
    secret = get_secret(vault_url, "db-password")
    print(f"Retrieved secret: {secret[:4]}{'*' * 8}")
