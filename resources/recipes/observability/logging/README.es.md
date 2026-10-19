# Logging en producción con Python, JavaScript y Java

Código de apoyo de la receta de StackPractices:
<https://stackpractices.com/es/recipes/logging/>

Logging estructurado por niveles con IDs de correlación y enmascarado de secretos.

## Archivos

| Archivo | Stack | Qué muestra |
| --- | --- | --- |
| `python_loguru.py` | Python + Loguru | Salida JSON (`serialize=True`), rotación, escrituras asíncronas (`enqueue=True`), enmascarado de secretos |
| `javascript_winston.js` | Node.js + Winston | Formato JSON, rotación por tamaño, campos de metadata, logger hijo para IDs de request |
| `java_slf4j.java` | Java + SLF4J/Logback | Mensajes parametrizados, IDs de correlación con `MDC`, logging de excepciones |

## Ejecutar

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

Java (requiere Maven):

```bash
mvn compile exec:java -Dexec.mainClass=UserService
```

Añade `%X{requestId}` al patrón del encoder en tu `logback.xml` para imprimir
el ID de correlación de MDC en cada línea.
