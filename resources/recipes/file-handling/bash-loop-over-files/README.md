# Bash Loop Over Files — Companion Resources

Runnable scripts for the [How to Loop Over Files in Bash recipe](https://stackpractices.com/recipes/bash-loop-over-files/): safe glob loops, `find -print0` pipelines, bulk renaming, `mapfile` arrays, `xargs` batching, and mtime-sorted iteration.

## Files

| File | Description |
| --- | --- |
| `loop-glob.sh` | Basic `for file in *.txt` loop with `[ -e ]` no-match guard |
| `find-print0-loop.sh` | Recursive `while IFS= read -r -d ''` over `find -print0` — survives spaces and newlines |
| `bulk-rename.sh` | Bulk rename `.jpeg` → `.jpg` with `nullglob` and `mv --` |
| `mapfile-read.sh` | Read a large file list into an array with `mapfile -d ''` |
| `xargs-batch.sh` | Parallel batch processing with `xargs -0 -P 4` |
| `sort-by-mtime.sh` | Iterate files newest-first with `find -printf` + `sort -z` |

## Quick start

```bash
mkdir -p demo && cd demo
touch {a,b,c}.txt "file with spaces.txt" report_{003,001,002}.txt

../loop-glob.sh            # counts .txt files, skips nothing
../find-print0-loop.sh .   # lists every file, spaces included
```

The scripts follow the rules the recipe teaches: quote every expansion, prefer `find -print0` over `ls`, enable `nullglob` when a glob may match nothing, and collect the list before mutating files.
