"""Output-side policy: PII redaction, dangerous code, URL allowlist.

URL policy parses the hostname properly - substring `in` checks let
"github.com.evil.com" through.
"""
import re
from urllib.parse import urlparse


class OutputValidator:
    SENSITIVE_PATTERNS = [
        (r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b", "[EMAIL REDACTED]"),
        (r"\b\d{3}-\d{2}-\d{4}\b", "[SSN REDACTED]"),
        (r"\b\d{4}[\s-]?\d{4}[\s-]?\d{4}[\s-]?\d{4}\b", "[CARD REDACTED]"),
        (r"sk-[A-Za-z0-9]{20,}", "[API KEY REDACTED]"),
    ]

    def validate(self, output: str) -> str:
        for pattern, replacement in self.SENSITIVE_PATTERNS:
            output = re.sub(pattern, replacement, output)
        return output


class OutputFilter:
    DANGEROUS_CODE = [
        r"os\.system\s*\(",
        r"subprocess\.(call|run|Popen)\s*\(",
        r"eval\s*\(",
        r"exec\s*\(",
        r"__import__\s*\(",
    ]
    ALLOWED_DOMAINS = ("stackoverflow.com", "github.com", "docs.python.org")

    def filter(self, output: str) -> tuple[str, bool]:
        for pattern in self.DANGEROUS_CODE:
            if re.search(pattern, output):
                return "[Dangerous code pattern filtered]", True

        for url in re.findall(r"https?://[^\s)\]]+", output):
            host = urlparse(url).hostname or ""
            if not any(host == d or host.endswith(f".{d}") for d in self.ALLOWED_DOMAINS):
                output = output.replace(url, "[URL FILTERED]")
        return output, False


if __name__ == "__main__":
    f = OutputFilter()
    for t in [
        "Run this: os.system('rm -rf /')",
        "See https://github.com/repo for the fix",
        "See https://github.com.evil.com for the fix",
    ]:
        print(f.filter(t))
