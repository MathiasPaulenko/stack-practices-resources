"""PII detection and redaction for RAG corpora."""

import re

PII_PATTERNS = {
    "email": r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b',
    "phone": r'\b\d{3}[-.]?\d{3}[-.]?\d{4}\b',
    "ssn": r'\b\d{3}-\d{2}-\d{4}\b',
    "credit_card": r'\b\d{4}[-\s]?\d{4}[-\s]?\d{4}[-\s]?\d{4}\b',
    "ip_address": r'\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b',
}


def detect_pii(text: str) -> dict:
    """Return a dict of PII type -> count found in text."""
    found = {}
    for pii_type, pattern in PII_PATTERNS.items():
        matches = re.findall(pattern, text)
        if matches:
            found[pii_type] = len(matches)
    return found


def redact_pii(text: str) -> str:
    """Replace PII matches with [REDACTED_TYPE] placeholders."""
    for pii_type, pattern in PII_PATTERNS.items():
        text = re.sub(pattern, f'[REDACTED_{pii_type.upper()}]', text)
    return text


if __name__ == "__main__":
    sample = "Contact jane@example.com or 555-123-4567. IP 10.0.0.1."
    print("Detected:", detect_pii(sample))
    print("Redacted:", redact_pii(sample))
