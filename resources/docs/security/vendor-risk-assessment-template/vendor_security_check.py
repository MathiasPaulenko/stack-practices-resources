"""Public security posture checks for vendor assessment.

Checks a vendor domain for DNSSEC, TLS grade, a published security.txt,
and breach history. Companion to the vendor risk assessment template.

Requires: requests. The breach check needs a paid Have I Been Pwned key
in the HIBP_API_KEY environment variable; without it that check is skipped.
"""

import os

import requests
from dataclasses import dataclass, field


@dataclass
class VendorSecurityCheck:
    vendor_name: str
    domain: str
    results: dict = field(default_factory=dict)

    def check_dnssec(self) -> None:
        """Check if the vendor domain has DNSSEC enabled."""
        try:
            resp = requests.get(
                f"https://dns.google/resolve?name={self.domain}&type=DNSKEY",
                timeout=10,
            )
            self.results["dnssec"] = (
                "enabled" if resp.json().get("Answer") else "disabled"
            )
        except Exception:
            self.results["dnssec"] = "error"

    def check_tls(self) -> None:
        """Check TLS configuration via the SSL Labs API."""
        try:
            resp = requests.get(
                f"https://api.ssllabs.com/api/v3/analyze?host={self.domain}"
                f"&all=done&ignoreMismatch=on",
                timeout=15,
            )
            data = resp.json()
            # The API is async: it returns a status until the scan finishes.
            if data.get("status") != "READY":
                self.results["tls_grade"] = f"pending ({data.get('status')})"
            else:
                grades = [e.get("grade") for e in data.get("endpoints", [])]
                self.results["tls_grade"] = min(g for g in grades if g)
        except Exception:
            self.results["tls_grade"] = "error"

    def check_security_txt(self) -> None:
        """Check for a published security contact file."""
        url = f"https://{self.domain}/.well-known/security.txt"
        try:
            resp = requests.head(url, timeout=10, allow_redirects=True)
            self.results["security_txt"] = (
                url if resp.status_code == 200 else "not found"
            )
        except Exception:
            self.results["security_txt"] = "not found"

    def check_breach_history(self) -> None:
        """Check domain breach history via Have I Been Pwned."""
        key = os.environ.get("HIBP_API_KEY")
        if not key:
            self.results["breaches"] = "skipped (no HIBP_API_KEY)"
            return
        try:
            resp = requests.get(
                "https://haveibeenpwned.com/api/v3/"
                f"breacheddomain/{self.domain}",
                headers={
                    "hibp-api-key": key,
                    "User-Agent": "VendorAssessment/1.0",
                },
                timeout=10,
            )
            if resp.status_code == 200:
                self.results["breach_count"] = len(resp.json())
            elif resp.status_code == 404:
                self.results["breach_count"] = 0
            else:
                self.results["breaches"] = f"error {resp.status_code}"
        except Exception:
            self.results["breach_count"] = "error"

    def run_all(self) -> dict:
        self.check_dnssec()
        self.check_tls()
        self.check_security_txt()
        self.check_breach_history()
        return self.results


if __name__ == "__main__":
    vendor = VendorSecurityCheck(
        vendor_name="Acme Cloud", domain="acmecloud.com"
    )
    for key, value in vendor.run_all().items():
        print(f"  {key}: {value}")
