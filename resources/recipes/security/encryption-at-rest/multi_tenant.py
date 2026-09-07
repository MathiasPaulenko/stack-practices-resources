"""Multi-tenant envelope encryption with KMS-managed KEKs.

Each tenant gets its own KMS key, ensuring cryptographic isolation.
Requires: pip install boto3 cryptography>=43.0
Python 3.12+
"""

import boto3
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
import base64
import os
from typing import Optional


class MultiTenantEncryption:
    """Per-tenant envelope encryption with KMS-managed KEKs."""

    def __init__(self, region: str = 'us-east-1'):
        self.kms = boto3.client('kms', region_name=region)

    def _get_tenant_kek_id(self, tenant_id: str) -> str:
        return f'arn:aws:kms:us-east-1:123456789012:key/tenant-{tenant_id}'

    def encrypt(self, tenant_id: str, plaintext: str, context: Optional[dict] = None) -> dict:
        kek_id = self._get_tenant_kek_id(tenant_id)
        dek = AESGCM.generate_key(bit_length=256)
        aesgcm = AESGCM(dek)
        nonce = os.urandom(12)
        aad = tenant_id.encode() if context is None else str(context).encode()
        ciphertext = aesgcm.encrypt(nonce, plaintext.encode(), aad)

        dek_response = self.kms.encrypt(
            KeyId=kek_id,
            Plaintext=dek,
            EncryptionContext={'tenant': tenant_id},
        )

        return {
            'ciphertext': base64.b64encode(ciphertext).decode(),
            'nonce': base64.b64encode(nonce).decode(),
            'encrypted_dek': base64.b64encode(dek_response['CiphertextBlob']).decode(),
            'tenant_id': tenant_id,
            'algorithm': 'AES256-GCM',
        }

    def decrypt(self, encrypted_package: dict) -> str:
        encrypted_dek = base64.b64decode(encrypted_package['encrypted_dek'])
        tenant_id = encrypted_package['tenant_id']

        dek_response = self.kms.decrypt(
            CiphertextBlob=encrypted_dek,
            EncryptionContext={'tenant': tenant_id},
        )
        dek = dek_response['Plaintext']

        aesgcm = AESGCM(dek)
        ciphertext = base64.b64decode(encrypted_package['ciphertext'])
        nonce = base64.b64decode(encrypted_package['nonce'])
        aad = tenant_id.encode()

        return aesgcm.decrypt(nonce, ciphertext, aad).decode()


if __name__ == '__main__':
    enc = MultiTenantEncryption()
    # Requires AWS credentials and tenant KMS keys.
    # encrypted = enc.encrypt('tenant-001', 'sensitive-data')
    # decrypted = enc.decrypt(encrypted)
    # print(f'Decrypted: {decrypted}')
    print('Multi-tenant encryption module loaded. Configure AWS credentials to run.')
