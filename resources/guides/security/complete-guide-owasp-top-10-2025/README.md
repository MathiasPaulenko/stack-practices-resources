# OWASP Top 10 2025 — Companion Files

Runnable mitigations for the categories in the guide
[Complete Guide to OWASP Top 10 2025](https://stackpractices.com/guides/complete-guide-owasp-top-10-2025/).

## Files

| File | Category | What it does |
| --- | --- | --- |
| `ssrf_protection.py` | A01 (SSRF folded into access control) | `SSRFProtector` validates user-supplied URLs by scheme, port, and **resolved IP** — the DNS answer is checked, not the URL string. Redirects are re-validated hop by hop. |
| `access_control.py` | A01 Broken Access Control | `require_ownership` / `require_role` decorators enforcing horizontal and vertical authorization server-side, plus a FastAPI adapter. |
| `security_logging.py` | A09 Logging & Alerting | `SecurityLogger` emits structured JSON events and trips an alert callback on failed-login bursts per IP and admin-route denials. |
| `fail_closed.py` | A10 Mishandling of Exceptional Conditions | Atomic `transfer_funds` with a rollback `transaction` context manager: expected failures raise typed errors, unexpected ones propagate — nothing fails open. |
| `test_mitigations.py` | all | pytest suite exercising each control. |

## Run

```bash
pip install pytest requests
pytest test_mitigations.py
```

## Notes

- The SSRF protector blocks private/link-local ranges **after DNS resolution** — validating the hostname string is useless when `evil.com` resolves to `169.254.169.254`.
- `access_control.py` is framework-agnostic; the commented FastAPI adapter shows how to wire it into `Depends`.
- In 2025, SSRF is no longer its own OWASP category — it lives under A01 Broken Access Control.
