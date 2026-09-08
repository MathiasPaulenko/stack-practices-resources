# Sentry Error Tracking — Ejemplos Companion

Este directorio contiene ejemplos de código companion para la guía de StackPractices
[Sentry: Triage y Resolución de Errores](https://stackpractices.com/es/guides/complete-guide-sentry-error-tracking/).

## Archivos

| Archivo | Lenguaje | Descripción |
|---------|----------|-------------|
| `sentry_config.py` | Python | Init del SDK de Sentry, filtrado de PII, captura manual (Flask/Django) |
| `sentry_node.ts` | TypeScript | Init del SDK de Sentry para Node.js (Express), spans custom |
| `SentryConfig.java` | Java | Config del SDK de Sentry para Spring Boot |
| `release_tracking.sh` | Bash | Creación de release, asociación de commits, upload de source maps |
| `alert_rules.yml` | YAML | Reglas de alerta de ejemplo (high error rate, errores nuevos, regresión de perf) |
| `test_sentry_examples.py` | Python | Tests para los ejemplos companion |

## Requisitos

- Python 3.10+ con `sentry-sdk` y `pytest` instalados
- Node.js 20+ con `@sentry/node` instalado
- Java 17+ con `sentry-spring-boot-starter` instalado
- `sentry-cli` instalado globalmente (`npm install -g @sentry/cli`)

## Ejecutar los Tests

```bash
pip install pytest sentry-sdk
pytest test_sentry_examples.py -v
```

Los tests verifican la estructura y sintaxis de los ejemplos. El test
`test_filter_sensitive_data_redacts_headers` requiere `sentry-sdk` instalado;
el resto corre sin dependencias externas.

## Uso

### Python (Flask/Django)

```python
from sentry_config import init_sentry
init_sentry()
```

### Node.js (Express)

```typescript
import { initSentry } from "./sentry_node";
initSentry();
```

### Java (Spring Boot)

Agregá `SentryConfig.java` al package de configuración de tu aplicación Spring Boot.

### Release Tracking

```bash
SENTRY_AUTH_TOKEN=your_token ./release_tracking.sh
```
