# Bash Parallel Execution — Companion Resources

Runnable scripts for the [Bash Parallel Execution recipe](https://stackpractices.com/recipes/bash-parallel-execution/): fan-out/fan-in with `xargs -P`, background-job pools with correct exit-code collection, and a counting semaphore for rate-limited calls.

## Files

| File | Description |
| --- | --- |
| `xargs-parallel.sh` | `xargs -P 4` over a file list with per-job logs; reports exit 123 correctly |
| `background-jobs.sh` | Job pool with `wait -n` slot management and per-PID `wait` for real exit codes |
| `semaphore.sh` | GNU parallel `sem` capping concurrent calls (requires GNU parallel) |

## Quick start

```bash
mkdir -p input && touch input/{a,b,c,d,e,f}.txt
./xargs-parallel.sh            # 6 files, 4 at a time
./background-jobs.sh           # 6 jobs, 3 slots — job 3 fails on purpose
printf '1\n2\n3\n4\n5\n' > ids.txt
./semaphore.sh                 # needs GNU parallel installed
```

The background-jobs script demonstrates the pattern the recipe warns about getting wrong: `pids+=($!)` at launch, then `wait "$pid"` per job — never `wait` then `jobs -p`, which returns nothing after the jobs are reaped.
