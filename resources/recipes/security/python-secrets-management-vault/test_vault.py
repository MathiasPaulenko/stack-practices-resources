"""Tests for Vault static and dynamic secret operations.

Run with: pytest test_vault.py -v

Requires the Vault CLI in PATH. The fixture starts a dev-mode server
on port 8200 with root token 'root' for the duration of the session.
"""
from __future__ import annotations

import os
import subprocess
import time

import hvac
import pytest


@pytest.fixture(scope="session")
def vault_client():
    proc = subprocess.Popen(
        ["vault", "server", "-dev", "-dev-root-token-id=root"],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        env={**os.environ, "VAULT_ADDR": "http://127.0.0.1:8200"},
    )
    time.sleep(1)
    client = hvac.Client(url="http://127.0.0.1:8200", token="root")
    assert client.is_authenticated()
    yield client
    proc.terminate()
    proc.wait()


def test_store_and_read_secret(vault_client):
    vault_client.secrets.kv.v2.create_or_update_secret(
        path="test/secret",
        secret={"api_key": "test-value"},
        mount_point="secret",
    )
    response = vault_client.secrets.kv.v2.read_secret_version(
        path="test/secret",
        mount_point="secret",
    )
    assert response["data"]["data"]["api_key"] == "test-value"


def test_list_secrets_returns_keys(vault_client):
    vault_client.secrets.kv.v2.create_or_update_secret(
        path="test/list/child",
        secret={"value": "1"},
        mount_point="secret",
    )
    result = vault_client.secrets.kv.v2.list_secrets(
        path="test/list",
        mount_point="secret",
    )
    assert "child" in result["data"]["keys"]


def test_list_secrets_invalid_path_returns_empty(vault_client):
    from static_secrets import list_secrets

    keys = list_secrets(vault_client, "nonexistent/path")
    assert keys == []


def test_secret_versioning(vault_client):
    vault_client.secrets.kv.v2.create_or_update_secret(
        path="test/versioned",
        secret={"value": "v1"},
        mount_point="secret",
    )
    vault_client.secrets.kv.v2.create_or_update_secret(
        path="test/versioned",
        secret={"value": "v2"},
        mount_point="secret",
    )

    latest = vault_client.secrets.kv.v2.read_secret_version(
        path="test/versioned",
        mount_point="secret",
    )
    assert latest["data"]["data"]["value"] == "v2"

    v1 = vault_client.secrets.kv.v2.read_secret_version(
        path="test/versioned",
        version=1,
        mount_point="secret",
    )
    assert v1["data"]["data"]["value"] == "v1"


def test_transit_encrypt_decrypt(vault_client):
    import base64

    vault_client.sys.enable_secrets_engine(backend_type="transit", path="transit")
    vault_client.write("transit/keys/test-key", {"type": "aes256-gcm96"})

    plaintext = "sensitive data"
    encoded = base64.b64encode(plaintext.encode()).decode()
    enc_response = vault_client.write("transit/encrypt/test-key", {"plaintext": encoded})
    ciphertext = enc_response["data"]["ciphertext"]

    dec_response = vault_client.write("transit/decrypt/test-key", {"ciphertext": ciphertext})
    decoded = base64.b64decode(dec_response["data"]["plaintext"]).decode()
    assert decoded == plaintext
