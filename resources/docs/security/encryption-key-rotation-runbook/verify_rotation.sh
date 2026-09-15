#!/bin/bash
# Verify encryption key rotation completion.
#
# Checks:
#   1. New KMS key is enabled
#   2. Old KMS key is disabled
#   3. Encryption/decryption works with new key
#
# Usage:
#   ./verify_rotation.sh

set -euo pipefail

NEW_KEY_ID="arn:aws:kms:us-east-1:123:key/new-key-id"
OLD_KEY_ID="arn:aws:kms:us-east-1:123:key/old-key-id"

# 1. Verify new key is enabled
NEW_KEY_STATE=$(aws kms describe-key --key-id "$NEW_KEY_ID" --query 'KeyMetadata.KeyState' --output text)
if [ "$NEW_KEY_STATE" != "Enabled" ]; then
    echo "FAIL: New key is not enabled (state: $NEW_KEY_STATE)"
    exit 1
fi
echo "OK: New key is enabled"

# 2. Verify old key is disabled
OLD_KEY_STATE=$(aws kms describe-key --key-id "$OLD_KEY_ID" --query 'KeyMetadata.KeyState' --output text)
if [ "$OLD_KEY_STATE" != "Disabled" ]; then
    echo "FAIL: Old key is not disabled (state: $OLD_KEY_STATE)"
    exit 1
fi
echo "OK: Old key is disabled"

# 3. Test encryption with new key
TEST_DATA="rotation-test-$(date +%s)"
ENCRYPTED=$(aws kms encrypt --key-id "$NEW_KEY_ID" --plaintext "$TEST_DATA" --output text --query CiphertextBlob)
DECRYPTED=$(aws kms decrypt --ciphertext-blob fileb://<(echo "$ENCRYPTED" | base64 --decode) --output text --query Plaintext | base64 --decode)
if [ "$DECRYPTED" != "$TEST_DATA" ]; then
    echo "FAIL: Encryption/decryption test failed"
    exit 1
fi
echo "OK: Encryption/decryption test passed"

echo "All verification checks passed."
