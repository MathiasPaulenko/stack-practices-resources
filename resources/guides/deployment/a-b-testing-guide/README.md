# A/B Testing Guide: Design, Statistics and Pitfalls

Companion resources for the guide [A/B Testing Guide: Design, Statistics and Pitfalls](https://stackpractices.com/guides/a-b-testing-guide/).

## Contents

| File | What it is |
|------|------------|
| `sample_size.py` | Sample size calculator for a two-proportion test (scipy): baseline rate, MDE, alpha and power in, users per group out |
| `assignment.py` | Deterministic user assignment by MD5 hash — same user always lands in the same bucket, independent across experiments |
| `analyze.py` | Two-proportion z-test analysis (statsmodels): rates, relative lift, p-value and significance flag |
| `hypothesis-template.md` | Pre-registration template: falsifiable hypothesis plus the pre-launch checklist (primary metric, guardrails, MDE, duration) |

## How to use

Run `sample_size.py` before launching a test to check your traffic can reach the required sample. Use `assignment.py` as the bucketing function (keyed on a stable user ID, never a cookie), and `analyze.py` at the pre-committed end date — not before. Fill in `hypothesis-template.md` and file it in your experiment registry before looking at any data.

Requires `scipy` and `statsmodels` (`pip install scipy statsmodels`).
