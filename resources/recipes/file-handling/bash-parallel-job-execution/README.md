# Parallel Job Control with Bash — Companion Examples

Runnable job-control scripts, companion to the
[Parallel Job Control with Bash recipe](https://stackpractices.com/recipes/bash-parallel-job-execution/) on StackPractices.

## Files

| File | What it shows |
| --- | --- |
| `job-control.sh` | GNU parallel wrapper: joblog, per-job timeout, `--halt` circuit breaker, summary + failed-job list |
| `xargs-exit-codes.sh` | Per-job result files with `xargs -P` when parallel isn't installed |
| `retry-backoff.sh` | Retries with exponential backoff and per-attempt timeout |
| `parallel_pool.py` | Same control natively in Python with `multiprocessing.Pool` |

## Quick start

```bash
# Create a demo input file
printf 'task-a\ntask-b\ntask-c\n' > jobs.txt

# GNU parallel wrapper — requires: apt install parallel
./job-control.sh 4 jobs.txt

# xargs variant — no extra dependencies
./xargs-exit-codes.sh 4 jobs.txt

# Retries — requires GNU parallel
./retry-backoff.sh 4 3 60 jobs.txt

# Python — jobs.txt must contain full shell commands
printf 'echo a && sleep 1\necho b && sleep 1\n' > jobs.txt
python parallel_pool.py
```

## Caveats

- `xargs -I {}` does **not** support GNU parallel's `{//}` basename syntax — use `basename` inside the `sh -c` wrapper, as shown.
- `--resume` / `--resume-failed` only work with a joblog from a previous run.
- `retry-backoff.sh` re-runs tasks; only use it for idempotent jobs.
