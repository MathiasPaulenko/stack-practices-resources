"""Normalize dynamic values before snapshot comparison.

Snapshots fail on every run when the output contains timestamps,
UUIDs, or random IDs. Replace them with stable placeholders so the
baseline only captures the parts that matter.
"""

import json
import re


def normalize_response(data: dict) -> str:
    """Serialize a dict to JSON with dynamic values replaced by placeholders."""
    text = json.dumps(data, indent=2)
    # UUIDs and generated ids
    text = re.sub(r'"id": "[^"]+"', '"id": "<UUID>"', text)
    text = re.sub(r'"transactionId": "[^"]+"', '"transactionId": "<TXN>"', text)
    # Timestamps
    text = re.sub(r'"createdAt": "[^"]+"', '"createdAt": "<TIMESTAMP>"', text)
    text = re.sub(r'"updatedAt": "[^"]+"', '"updatedAt": "<TIMESTAMP>"', text)
    return text
