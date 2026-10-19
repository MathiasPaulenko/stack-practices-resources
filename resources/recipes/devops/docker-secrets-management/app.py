"""Read secrets with the _FILE convention, with optional Vault/AWS backends."""
import json
import os
import time


def get_secret(name: str) -> str:
    """Read a secret from a file (Docker Swarm/Compose pattern).

    Falls back to the plain environment variable for local development.
    """
    file_path = os.environ.get(f"{name}_FILE")
    if file_path:
        with open(file_path, "r") as f:
            return f.read().strip()
    return os.environ.get(name, "")


def get_vault_secret(path: str) -> dict:
    """Fetch a secret from HashiCorp Vault (pip install hvac)."""
    import hvac

    client = hvac.Client(
        url=os.environ["VAULT_ADDR"],
        token=get_secret("VAULT_TOKEN"),
    )
    result = client.secrets.kv.v2.read_secret_version(path=path)
    return result["data"]["data"]


def get_aws_secret(secret_name: str, region: str = "us-east-1") -> dict:
    """Fetch a secret from AWS Secrets Manager (pip install boto3)."""
    import boto3

    client = boto3.client("secretsmanager", region_name=region)
    response = client.get_secret_value(SecretId=secret_name)
    return json.loads(response["SecretString"])


_secret_cache: dict[str, tuple[float, str]] = {}


def get_cached_secret(name: str, ttl: int = 300) -> str:
    """In-memory cache so Vault/AWS lookups don't run on every request."""
    if name in _secret_cache:
        cached_time, value = _secret_cache[name]
        if time.time() - cached_time < ttl:
            return value
    value = get_secret(name)
    _secret_cache[name] = (time.time(), value)
    return value


if __name__ == "__main__":
    print("DB password loaded:", bool(get_secret("DB_PASSWORD")))
