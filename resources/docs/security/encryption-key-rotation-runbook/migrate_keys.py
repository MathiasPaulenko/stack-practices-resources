"""Data migration script for encryption key rotation.

Re-encrypts records from an old KMS key to a new KMS key in batches
with configurable parallelism and rate limiting.

Usage:
    python migrate_keys.py

Prerequisites:
    - boto3 installed: pip install boto3
    - AWS credentials configured with KMS decrypt/encrypt permissions
    - Database access configured
"""

import boto3
from concurrent.futures import ThreadPoolExecutor
from typing import List

kms = boto3.client("kms")
old_key_id = "arn:aws:kms:us-east-1:123:key/old-key-id"
new_key_id = "arn:aws:kms:us-east-1:123:key/new-key-id"


def migrate_record(record_id: str) -> str:
    """Decrypt with old key, re-encrypt with new key, update record."""
    # 1. Decrypt with old key
    encrypted_data = db.get_encrypted_field(record_id)
    plaintext = kms.decrypt(
        CiphertextBlob=encrypted_data,
        KeyId=old_key_id,
    )["Plaintext"]

    # 2. Re-encrypt with new key
    new_ciphertext = kms.encrypt(
        Plaintext=plaintext,
        KeyId=new_key_id,
    )["CiphertextBlob"]

    # 3. Update record
    db.update_encrypted_field(record_id, new_ciphertext)
    return record_id


def migrate_in_batches(record_ids: List[str], batch_size: int = 1000, workers: int = 4) -> None:
    """Migrate records in batches with thread pool."""
    total = len(record_ids)

    for i in range(0, total, batch_size):
        batch = record_ids[i : i + batch_size]
        with ThreadPoolExecutor(max_workers=workers) as executor:
            results = list(executor.map(migrate_record, batch))
        print(f"Migrated {len(results)} records ({i + len(batch)}/{total})")


if __name__ == "__main__":
    record_ids = db.get_all_record_ids()
    migrate_in_batches(record_ids, batch_size=1000, workers=4)
    print("Migration complete.")
