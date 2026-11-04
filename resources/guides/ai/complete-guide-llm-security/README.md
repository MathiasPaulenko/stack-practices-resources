# Complete Guide to LLM Security - Code Examples

Runnable defense layers from the guide:
<https://stackpractices.com/guides/complete-guide-llm-security/>

## Setup

```bash
pip install -r requirements.txt
export OPENAI_API_KEY=sk-...   # only needed for live red-teaming
```

## Files

| File | What it shows |
| --- | --- |
| `injection_guard.py` | Regex tripwire for known injection phrasings (signal, not verdict) |
| `document_sanitizer.py` | Strips hidden-instruction carriers from retrieved docs |
| `jailbreak_detector.py` | Heuristic jailbreak signal (DAN, roleplay, authority, probing) |
| `output_filter.py` | PII redaction + dangerous-code + parsed-domain URL policy |
| `rate_limiter.py` | Sliding-window limiter on requests AND tokens (wallet-DoS) |
| `tool_validator.py` | Tool allowlist + argument validation + session scoping |
| `security_harness.py` | Runs the static attack corpus through the layers |
| `attack_corpus.json` | Attack + benign strings with expected outcomes |

## Offline check

```bash
python security_harness.py --verbose
```

No API calls required - the corpus runs purely through the defense
layers. The guide's `LLMRedTeam` class extends this with generated
attacks against a live pipeline.
