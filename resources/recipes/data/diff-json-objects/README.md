# Diff JSON Objects — Companion Files

Runnable diffs for the StackPractices recipe:
[Diff JSON Objects](https://stackpractices.com/recipes/diff-json-objects/)

| File | What it is |
|------|-----------|
| `json_diff.py` | Dependency-free recursive diff in Python — prints added/removed/changed paths |
| `diff-json.js` | Same recursive walk in Node, plus `--patch` mode for RFC 6902 output via `fast-json-patch` |
| `JsonDiff.java` | Recursive diff over the Jackson tree (needs `jackson-databind` on the classpath) |
| `staging.json` / `prod.json` | Sample payloads — a config that drifted between environments |

## Quick start

```bash
# Python, no dependencies
python json_diff.py staging.json prod.json

# Node, no dependencies
node diff-json.js staging.json prod.json

# Node, RFC 6902 patch
npm install fast-json-patch
node diff-json.js --patch staging.json prod.json

# Java (requires jackson jars on the classpath)
javac -cp "jackson-databind.jar;jackson-core.jar;jackson-annotations.jar" JsonDiff.java
java -cp ".;jackson-databind.jar;jackson-core.jar;jackson-annotations.jar" JsonDiff staging.json prod.json
```

Expected output on the sample files: three changes — `/db/host`
changed, `/features/1` added, `/logLevel` added.
