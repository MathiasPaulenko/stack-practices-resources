# Flatten and Unflatten Nested Objects — Companion Examples

Runnable examples for flattening and unflattening nested objects in Python, JavaScript, and Java.

## Files

| File | Language | What it does |
| --- | --- | --- |
| `flatten.py` | Python | Flatten/unflatten with regex-based key splitting |
| `flatten.js` | JavaScript (Node.js) | Flatten/unflatten with RegExp key splitting |
| `FlattenUtil.java` | Java | Flatten/unflatten with LinkedHashMap and List |
| `sample.json` | JSON | Sample nested object for testing |

## Running

### Python

```bash
python flatten.py
```

### JavaScript

```bash
node flatten.js
```

### Java

```bash
javac FlattenUtil.java
java FlattenUtil
```

## Expected output

Each script prints the flattened key-value pairs, the unflattened (restored) object, and verifies that the round-trip `flatten(unflatten(flat)) == flat` holds.

## Source

- [Flatten and Unflatten Nested Objects](https://stackpractices.com/recipes/flatten-unflatten-objects/)
