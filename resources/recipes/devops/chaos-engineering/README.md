# Chaos Engineering — Fault Injection & Game Day Kit

Runnable companion code for the StackPractices recipe
[Chaos Engineering](https://stackpractices.com/recipes/chaos-engineering/).

## Files

| File | What it shows |
| --- | --- |
| `src/litmus-pod-delete.yaml` | Litmus `ChaosEngine` manifest: pod-delete experiment scoped to a deployment. |
| `src/inject-latency.sh` | `tc netem` latency injection (500ms for 60s) with cleanup. |
| `src/toxiproxy-setup.sh` | Toxiproxy proxy + latency/timeout toxics for a MySQL dependency. |
| `src/gremlin-attacks.sh` | Gremlin CLI attacks: CPU stress, blackhole, memory. |
| `src/steady-state-check.py` | SLO checker to run before/during/after experiments (health + metrics endpoints). |
| `src/game-day-template.md` | Game day runbook template: participants, scope, experiments, abort criteria, rollback. |

## Usage

```bash
sudo ./src/inject-latency.sh        # needs root (tc)
python src/steady-state-check.py    # exit 0 = safe to experiment
kubectl apply -f src/litmus-pod-delete.yaml
```

## Related

- Recipe (EN): <https://stackpractices.com/recipes/chaos-engineering/>
- Recipe (ES): <https://stackpractices.com/es/recipes/chaos-engineering/>
- Guide: <https://stackpractices.com/guides/chaos-engineering-guide/>
