# Patrón Async Generator — Código Companion

Recursos companion para el [Patrón Async Generator](https://stackpractices.com/es/patterns/async-generator-pattern/) en StackPractices.com.

## Archivos

| Archivo | Lenguaje | Descripción |
|---------|----------|-------------|
| `python_async_generator.py` | Python | Async generator con aiohttp, líneas de archivo y early exit |
| `javascript_async_generator.js` | JavaScript | Async generator con fetch y fs/promises |
| `java_lazy_stream.java` | Java | Lazy Stream con HttpClient y Jackson |
| `test_async_generator.py` | Python | Tests pytest-asyncio (correctitud, data vacía, early exit) |
| `test_async_generator.js` | JavaScript | Tests Jest (correctitud, data vacía, early exit) |
| `docker-compose.yml` | Docker | Mock API server para testing local |
| `requirements.txt` | Python | Dependencias Python |
| `package.json` | Node.js | Dependencias Node.js y script de test |

## Cómo ejecutar

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

Compilar y correr con Java 21+:

```bash
javac -cp ".:jackson-databind.jar:jackson-core.jar:jackson-annotations.jar" java_lazy_stream.java
java -cp ".:jackson-databind.jar:jackson-core.jar:jackson-annotations.jar" LazyStream
```
