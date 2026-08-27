# Analizar Archivos de Log

Recurso complementario de [Analizar Archivos de Log](https://stackpractices.com/es/recipes/parse-log-files/).

## Archivos

| Archivo | Descripción |
|---------|-------------|
| `access.log` | Líneas de ejemplo de logs de acceso combinados de Apache/Nginx |
| `app.jsonl` | Logs de aplicación de ejemplo en formato JSON Lines |
| `syslog.log` | Mensajes BSD syslog (RFC 3164) de ejemplo |
| `parse_log.py` | Analiza logs de acceso Apache/Nginx con Python y `re` |
| `parse_log.js` | Analiza logs de acceso Apache/Nginx con streams de Node.js |
| `LogParser.java` | Analiza logs de acceso Apache/Nginx con regex de Java |
| `parse_jsonl.py` | Analiza logs JSON Lines con Python |
| `parse_syslog.py` | Analiza mensajes syslog BSD con Python |

## Uso

### Python

```bash
python parse_log.py
python parse_jsonl.py
python parse_syslog.py
```

### JavaScript

```bash
node parse_log.js
```

### Java

```bash
javac LogParser.java && java LogParser
```
