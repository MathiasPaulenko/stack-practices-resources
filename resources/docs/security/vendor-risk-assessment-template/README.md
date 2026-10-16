# Vendor Risk Assessment Template — Companion Files

Companion resources for the article
[Vendor Risk Assessment Template](https://stackpractices.com/docs/vendor-risk-assessment-template/)
on StackPractices.

## Contents

- `assessment-workbook.md` — the full assessment template, copy-paste ready.
- `vendor_security_check.py` — public posture checks for a vendor domain (DNSSEC, SSL Labs TLS grade, `security.txt`, HIBP breach history).
- `vendor_risk_scorer.py` — weighted risk scoring and decision bands matching the workbook.
- `vendor_monitor.py` — reads `vendor-registry.yaml` and runs posture checks for every vendor.
- `vendor-monitoring.yml` — GitHub Actions workflow that runs the monitor weekly.
- `vendor-registry.yaml` — vendor registry format for the monitor.

## Usage

```bash
pip install requests pyyaml

# Score a completed assessment
python vendor_risk_scorer.py

# Check one vendor's public posture
python vendor_security_check.py

# Monitor the whole registry (fails on degradation of high-risk vendors)
HIBP_API_KEY=<key> python vendor_monitor.py --config vendor-registry.yaml
```

The SSL Labs API is asynchronous — the first call returns a status (`IN_PROGRESS`) instead of a grade; poll `analyze?host=<domain>&all=done` until `status == "READY"`. The HIBP `/breacheddomain` endpoint requires a paid API key in `HIBP_API_KEY`; without it that check is skipped.

## License

Free to use and adapt under MIT. Attribution appreciated, not required.
