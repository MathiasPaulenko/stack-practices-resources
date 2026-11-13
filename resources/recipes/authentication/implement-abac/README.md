# Implement ABAC — Companion

Companion code for the StackPractices recipe [Implement ABAC](https://stackpractices.com/recipes/implement-abac/).

## Files

- `evaluate_policy.py` — minimal ABAC policy evaluator (stdlib only). First-match rule ordering, `${subject.x}` attribute references, `_lt`/`_gt` comparators, deny-by-default.
- `policy.json` — example policy: deny top-secret from external networks, deny after hours, allow editors to read their own department.

## Usage

```bash
python evaluate_policy.py --demo                      # built-in policy + scenarios
python evaluate_policy.py policy.json request.json    # your own policy + request
```

## Sample output

```
decision: ALLOW  (rule: editors-read-own-department)
  deny-top-secret scenario: DENY (rule: deny-top-secret-outside-office)
  cross-department scenario: DENY (rule: (default))
  after-hours scenario: DENY (rule: business-hours-only)
```

Rule order matters: this evaluator uses first-match semantics, so deny rules
should come before broad allow rules.
