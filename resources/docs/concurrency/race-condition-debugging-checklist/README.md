# Race Condition Debugging Checklist — Companion

Runnable reproductions and fixes for the
[race condition debugging checklist](https://stackpractices.com/docs/race-condition-debugging-checklist/).
Each file maps to a section of the checklist, so you can trigger the race,
watch the detector report it, then verify the fix silences it.

## Files

| File | Language | Checklist section | What it does |
|------|----------|-------------------|--------------|
| `stress_counter.py` | Python | 2.1 | Hammers a non-atomic counter from 100 threads; a short count means lost updates |
| `barrier_repro.py` | Python | 2.2 | `threading.Barrier` forces two threads to start at once — deterministic interleaving |
| `RaceConditionStress.java` | Java (jcstress) | 2.3 | Memory-model test; the "0, 0" outcome is forbidden — a real execution, not theory |
| `counter_race.go` | Go | 3.2 | Unsynchronized increment; run with `go run -race` to see the report |
| `counter_fix.go` | Go | 4.2 / 5.1 | The same counter behind a mutex; `-race` stays silent |

## Run them

```bash
python stress_counter.py        # expect "LOST n updates" on most runs
python barrier_repro.py         # prints how often the reader missed the write
go run -race counter_race.go    # WARNING: DATA RACE with two stacks
go run -race counter_fix.go     # clean; always 100000
# RaceConditionStress.java needs the jcstress harness:
# https://openjdk.org/projects/code-tools/jcstress/
```

## Notes

- `stress_counter.py` and `barrier_repro.py` need only Python 3.8+.
- `counter_*.go` needs Go 1.20+; the `-race` flag requires CGO enabled.
- Races are timing-dependent: a clean run proves nothing. Loop the repros,
  run them under a race detector, and treat every flagged interleaving as a
  real bug.
