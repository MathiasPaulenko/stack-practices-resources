"""Searchable encryption with blind index using HMAC.

Encrypt data while supporting exact-match queries via a blind index.
Requires: pip install cryptography>=43.0
Python 3.12+
"""

import hmac
import hashlib
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
import os


class SearchableEncryption:
    """Encrypt data while supporting exact-match queries via blind index."""

    def __init__(self, encryption_key: bytes, index_key: bytes):
        self.encryption_key = encryption_key
        self.index_key = index_key

    def _blind_index(self, value: str) -> str:
        return hmac.new(
            self.index_key, value.encode(), hashlib.sha256
        ).hexdigest()

    def encrypt(self, plaintext: str) -> dict:
        aesgcm = AESGCM(self.encryption_key)
        nonce = os.urandom(12)
        ciphertext = aesgcm.encrypt(nonce, plaintext.encode(), None)

        return {
            'ciphertext': ciphertext.hex(),
            'nonce': nonce.hex(),
            'blind_index': self._blind_index(plaintext),
        }

    def decrypt(self, encrypted: dict) -> str:
        aesgcm = AESGCM(self.encryption_key)
        nonce = bytes.fromhex(encrypted['nonce'])
        ciphertext = bytes.fromhex(encrypted['ciphertext'])
        return aesgcm.decrypt(nonce, ciphertext, None).decode()


if __name__ == '__main__':
    enc_key = os.urandom(32)
    idx_key = os.urandom(32)
    se = SearchableEncryption(enc_key, idx_key)

    pkg = se.encrypt('user@example.com')
    print(f'Blind index: {pkg["blind_index"]}')
    print(f'Ciphertext: {pkg["ciphertext"][:40]}...')

    plain = se.decrypt(pkg)
    print(f'Decrypted: {plain}')
