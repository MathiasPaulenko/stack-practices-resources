# Parse Server Log Files

Companion resource for [Parse Server Log Files](https://stackpractices.com/recipes/parse-log-files/).

## Files

| File | Description |
|------|-------------|
| `access.log` | Sample Apache/Nginx combined access log lines |
| `app.jsonl` | Sample application logs in JSON Lines format |
| `syslog.log` | Sample BSD syslog (RFC 3164) messages |
| `parse_log.py` | Parse Apache/Nginx access logs with Python and `re` |
| `parse_log.js` | Parse Apache/Nginx access logs with Node.js streams |
| `LogParser.java` | Parse Apache/Nginx access logs with Java regex |
| `parse_jsonl.py` | Parse JSON Lines logs with Python |
| `parse_syslog.py` | Parse BSD syslog messages with Python |

## Usage

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
