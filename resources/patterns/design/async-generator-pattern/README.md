# Async Generator Pattern — Companion Code

Companion resources for the [Async Generator Pattern](https://stackpractices.com/patterns/async-generator-pattern/) on StackPractices.com.

## Files

| File | Language | Description |
|------|----------|-------------|
| `python_async_generator.py` | Python | Async generator with aiohttp, file lines, and early exit |
| `javascript_async_generator.js` | JavaScript | Async generator with fetch and fs/promises |
| `java_lazy_stream.java` | Java | Lazy Stream with HttpClient and Jackson |
| `test_async_generator.py` | Python | pytest-asyncio tests (correctness, empty data, early exit) |
| `test_async_generator.js` | JavaScript | Jest tests (correctness, empty data, early exit) |
| `docker-compose.yml` | Docker | Mock API server for local testing |
| `requirements.txt` | Python | Python dependencies |
| `package.json` | Node.js | Node.js dependencies and test script |

## Running

### Python

```bash
pip install -r requirements.txt
pytest test_async_generator.py -v
```

### JavaScript

```bash
npm install
npm test
```

### Java

Compile and run with Java 21+:

```bash
javac -cp ".:jackson-databind.jar:jackson-core.jar:jackson-annotations.jar" java_lazy_stream.java
java -cp ".:jackson-databind.jar:jackson-core.jar:jackson-annotations.jar" LazyStream
```
