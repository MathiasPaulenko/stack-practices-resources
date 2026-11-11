# Generate Temporary Files — companion code

Runnable versions of the four implementations from the
[Generate Temporary Files](https://stackpractices.com/recipes/generate-temporary-files/)
recipe on StackPractices. Each one shows the three guarantees a temp API must
give you: an unpredictable name, atomic creation, and deterministic cleanup.

## Layout

| Path | What it shows |
| --- | --- |
| `python/temp_files.py` | `NamedTemporaryFile`, `TemporaryDirectory`, `mkstemp`, `fsync` + atomic `os.replace`, recursive `shutil.rmtree` |
| `node/temp_files.js` | `fs.mkdtemp`, crypto-random names with exclusive `wx` create, `tmp` package exit hooks |
| `java/TempFileExample.java` | `Files.createTempFile` / `createTempDirectory`, `deleteOnExit` registration order, `Files.walk` in try-with-resources |
| `bash/temp_files.sh` | `mktemp` / `mktemp -d`, one `trap cleanup EXIT` that preserves the real exit status |

## Run

```bash
python python/temp_files.py

cd node && npm install && node temp_files.js

cd java && javac TempFileExample.java && java TempFileExample

bash bash/temp_files.sh
```

No build step, no services — every script cleans up after itself.
