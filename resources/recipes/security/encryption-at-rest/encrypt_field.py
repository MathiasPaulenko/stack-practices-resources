"""Envelope encryption with AWS KMS using AES-256-GCM.

Requires: pip install boto3 cryptography>=43.0
Python 3.12+
"""

import boto3
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
import base64
import os

kms = boto3.client('kms')


def encrypt_field(plaintext: str, kms_key_id: str) -> dict:
    dek = AESGCM.generate_key(bit_length=256)
    aesgcm = AESGCM(dek)
    nonce = os.urandom(12)
    ciphertext = aesgcm.encrypt(nonce, plaintext.encode(), None)

    dek_response = kms.encrypt(KeyId=kms_key_id, Plaintext=dek)
    encrypted_dek = base64.b64encode(dek_response['CiphertextBlob']).decode()

    return {
        "ciphertext": base64.b64encode(ciphertext).decode(),
        "nonce": base64.b64encode(nonce).decode(),
        "encrypted_dek": encrypted_dek,
        "algorithm": "AES256-GCM",
    }


def decrypt_field(encrypted_package: dict, kms_key_id: str) -> str:
    encrypted_dek = base64.b64decode(encrypted_package['encrypted_dek'])
    dek_response = kms.decrypt(CiphertextBlob=encrypted_dek)
    dek = dek_response['Plaintext']

    aesgcm = AESGCM(dek)
    ciphertext = base64.b64decode(encrypted_package['ciphertext'])
    nonce = base64.b64decode(encrypted_package['nonce'])

    return aesgcm.decrypt(nonce, ciphertext, None).decode()


if __name__ == '__main__':
    # Quick smoke test (requires AWS credentials and a KMS key)
    import json
    key_id = os.environ.get('KMS_KEY_ID', 'alias/aws/ebs')
    pkg = encrypt_field('hello world', key_id)
    print(json.dumps(pkg, indent=2))
    plain = decrypt_field(pkg, key_id)
    print(f'Decrypted: {plain}')
