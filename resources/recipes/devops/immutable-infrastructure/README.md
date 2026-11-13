# Immutable Infrastructure — Companion

Companion code for the StackPractices recipe [Immutable Infrastructure](https://stackpractices.com/recipes/immutable-infrastructure/).

## Files

- `check_immutable.py` — static checker (stdlib only) that audits Docker Compose / Kubernetes manifests for immutability violations: `:latest` tags, missing digest pins, writable root filesystems, exposed SSH, `hostPath` volumes, privileged containers.

## Usage

```bash
python check_immutable.py --demo              # run against a built-in violating sample
python check_immutable.py deployment.yaml     # audit your own manifests
```

Exit code is `1` when violations are found, so it can gate a CI job:

```yaml
- name: Enforce immutability
  run: python check_immutable.py k8s/*.yaml
```

## Sample output

```
demo.yaml:8 [LATEST_TAG] image uses :latest tag (mutable): image: myregistry.com/api:latest
demo.yaml:12 [PRIVILEGED] privileged container can mutate the host: privileged: true
4 violation(s) across 1 file(s)
```
