# Production Logging in Python, JavaScript and Java

Companion code for the StackPractices recipe:
<https://stackpractices.com/recipes/logging/>

Structured, level-based logging with correlation IDs and secret redaction.

## Files

| File | Stack | What it shows |
| --- | --- | --- |
| `python_loguru.py` | Python + Loguru | JSON output (`serialize=True`), rotation, async writes (`enqueue=True`), secret masking |
| `javascript_winston.js` | Node.js + Winston | JSON format, size-based rotation, metadata fields, child logger for request IDs |
| `java_slf4j.java` | Java + SLF4J/Logback | Parameterized messages, `MDC` correlation IDs, exception logging |

## Run

Python:

```bash
pip install -r requirements.txt
python python_loguru.py
```

JavaScript:

```bash
npm install
node javascript_winston.js
```

Java (needs Maven):

```bash
mvn compile exec:java -Dexec.mainClass=UserService
```

Add `%X{requestId}` to your `logback.xml` encoder pattern to print the MDC
correlation ID on every line.
