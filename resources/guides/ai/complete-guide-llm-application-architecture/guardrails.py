"""Input/output guardrails: length, injection patterns, PII redaction."""
import re
from dataclasses import dataclass


@dataclass
class GuardrailResult:
    passed: bool
    reason: str = ""


class InputGuardrail:
    def __init__(self, max_length: int = 10000, blocked_patterns: list[str] | None = None):
        self.max_length = max_length
        self.blocked_patterns = [re.compile(p, re.IGNORECASE) for p in (blocked_patterns or [])]

    def check(self, text: str) -> GuardrailResult:
        if len(text) > self.max_length:
            return GuardrailResult(False, f"Input exceeds max length of {self.max_length}")
        for pattern in self.blocked_patterns:
            if pattern.search(text):
                return GuardrailResult(False, f"Input matches blocked pattern: {pattern.pattern}")
        return GuardrailResult(True)


class OutputGuardrail:
    def __init__(self):
        self.pii_patterns = [
            (re.compile(r"\b\d{3}-\d{2}-\d{4}\b"), "[SSN REDACTED]"),
            (re.compile(r"\b\d{16}\b"), "[CARD REDACTED]"),
            (re.compile(r"\b[\w.]+@[\w]+\.\w+\b"), "[EMAIL REDACTED]"),
        ]

    def redact_pii(self, text: str) -> str:
        for pattern, replacement in self.pii_patterns:
            text = pattern.sub(replacement, text)
        return text


INPUT_GUARDRAIL = InputGuardrail(
    max_length=5000,
    blocked_patterns=[
        r"ignore (previous|above) instructions",
        r"disregard (your|the) system prompt",
        r"reveal (your|the) (system|initial) prompt",
    ],
)
