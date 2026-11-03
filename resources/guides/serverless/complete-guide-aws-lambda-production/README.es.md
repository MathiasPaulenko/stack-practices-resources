# Guía Completa de AWS Lambda en Producción — Código de acompañamiento

Bloques ejecutables para la guía
[Guía Completa de AWS Lambda en Producción](https://stackpractices.com/es/guides/complete-guide-aws-lambda-production/)
de StackPractices.

## Archivos

| Archivo | Qué implementa |
| --- | --- |
| `cold_start_tracker.py` | Instrumentación de init vs handler |
| `structured_logger.py` | Logging JSON con `request_id` en cada línea |
| `rds_proxy_client.py` | Conexión RDS Proxy con limpieza en `finally` |
| `secrets_cache.py` | Secrets Manager + caché con `lru_cache` |
| `idempotent_handler.py` | Clave de idempotencia por hash del evento + Redis |
| `sqs_batch_handler.py` | `batchItemFailures` para reintentos parciales |
| `template.yaml` | Plantilla SAM: alias + canary + alarma de rollback |
| `deploy-canary.sh` | Script de desplazamiento de tráfico por alias |
| `test_lambda_patterns.py` | Tests de humo con pytest (fakeredis, mocks) |

## Puesta en marcha

```bash
pip install -r requirements.txt
pip install fakeredis pytest
pytest test_lambda_patterns.py -v
```

Las dependencias que aporta tu app (`redis_client`, `process_event`,
`process_message`, `secret`) se inyectan para que los módulos sean testeables
sin credenciales de AWS.
