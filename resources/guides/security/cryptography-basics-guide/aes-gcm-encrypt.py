"""AES-256-GCM encryption: low-level control over key and nonce.

Run: pip install cryptography && python aes-gcm-encrypt.py
"""
import os
from cryptography.hazmat.primitives.ciphers.aead import AESGCM


def encrypt(key: bytes, plaintext: bytes, aad: bytes = b"") -> dict:
    """Encrypt with AES-256-GCM. The nonce must be unique per key — never reuse."""
    nonce = os.urandom(12)  # 96-bit random nonce
    aesgcm = AESGCM(key)
    ciphertext = aesgcm.encrypt(nonce, plaintext, aad)
    return {"nonce": nonce, "ciphertext": ciphertext, "aad": aad}


def decrypt(key: bytes, nonce: bytes, ciphertext: bytes, aad: bytes = b"") -> bytes:
    """Raises InvalidTag if the ciphertext, nonce, key, or AAD was altered."""
    return AESGCM(key).decrypt(nonce, ciphertext, aad)


if __name__ == "__main__":
    key = AESGCM.generate_key(bit_length=256)
    blob = encrypt(key, b"sensitive data", aad=b"context:v1")
    print("ciphertext:", blob["ciphertext"].hex()[:48], "...")
    print("decrypted:", decrypt(key, blob["nonce"], blob["ciphertext"], blob["aad"]))
