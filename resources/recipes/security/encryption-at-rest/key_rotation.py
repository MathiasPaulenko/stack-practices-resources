"""Key rotation with zero-downtime re-encryption using AWS KMS.

Rotate the master key and re-encrypt data in batches without downtime.
Requires: pip install boto3
Python 3.12+
"""

import boto3
import base64
from typing import Callable


class KeyRotation:
    """Rotate KMS master keys with zero-downtime re-encryption."""

    def __init__(self, old_key_id: str, new_key_id: str):
        self.kms = boto3.client('kms')
        self.old_key_id = old_key_id
        self.new_key_id = new_key_id

    def re_encrypt_record(self, encrypted_package: dict) -> dict:
        encrypted_dek = base64.b64decode(encrypted_package['encrypted_dek'])
        response = self.kms.re_encrypt(
            CiphertextBlob=encrypted_dek,
            DestinationKeyId=self.new_key_id,
        )
        encrypted_package['encrypted_dek'] = base64.b64encode(
            response['CiphertextBlob']
        ).decode()
        return encrypted_package

    def batch_re_encrypt(
        self,
        fetch_fn: Callable[[int], list[dict]],
        save_fn: Callable[[dict], None],
        batch_size: int = 100,
    ):
        offset = 0
        while True:
            records = fetch_fn(batch_size)
            if not records:
                break

            for record in records:
                re_encrypted = self.re_encrypt_record(record)
                save_fn(re_encrypted)

            offset += len(records)
            print(f'Re-encrypted {offset} records')


if __name__ == '__main__':
    # Requires AWS credentials and KMS keys.
    # rotation = KeyRotation(
    #     old_key_id='arn:aws:kms:us-east-1:123:key/old-key',
    #     new_key_id='arn:aws:kms:us-east-1:123:key/new-key',
    # )
    # rotation.batch_re_encrypt(fetch_records, update_record, batch_size=500)
    print('Key rotation module loaded. Configure AWS credentials to run.')
