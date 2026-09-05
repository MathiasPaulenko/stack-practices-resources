# Feature Flags: Rollout, Targeting, and Safe Rollback

Companion resource for [Feature Flags recipe](https://stackpractices.com/recipes/feature-flags/).

## Files

| File | Description |
|------|-------------|
| `feature_flags.py` | Python flag service with boolean, percentage, user, and group rollouts |
| `feature_flags.js` | JavaScript flag service (ES module) |
| `FeatureFlags.java` | Java flag service |
| `rollout_plan.py` | Staged rollout plan for gradually increasing flag percentage |
| `ab_test.js` | A/B test variant assignment with deterministic bucketing |
| `launchdarkly_example.py` | LaunchDarkly managed client example |
| `test_feature_flags.py` | pytest tests for the Python flag service |

## Quick start

### Python

```bash
python feature_flags.py
```

### JavaScript

```bash
node feature_flags.js
```

### Java

```bash
javac FeatureFlags.java && java FeatureFlags
```

### Run tests

```bash
pip install pytest
pytest test_feature_flags.py -v
```

### A/B test simulation

```bash
node ab_test.js
```

### Rollout plan simulation

```bash
python rollout_plan.py
```

### LaunchDarkly example

```bash
pip install ldclient
export LAUNCHDARKLY_SDK_KEY="your-sdk-key"
python launchdarkly_example.py
```

## License

MIT
