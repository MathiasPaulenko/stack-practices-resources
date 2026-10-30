# Runbook de precalentamiento de caché — Companion

Companion del doc de StackPractices [Runbook de precalentamiento de caché](https://stackpractices.com/es/docs/cache-warmup-runbook/).

## Archivos

| Archivo | Propósito | Ejecución |
| --- | --- | --- |
| `src/hot_keys.py` | Genera `hot-keys.json` desde logs de acceso JSONL o stats LFU de Redis (`OBJECT FREQ`), agrupadas por nivel de prioridad. | `python3 src/hot_keys.py --logs access.jsonl --output hot-keys.json` |
| `src/warmup.py` | Runner de warmup por niveles: health check, lotes con pausas y verificación de cobertura. Incluye un loader `--demo` para probar sin base de datos. | `python3 src/warmup.py --keys hot-keys.json --redis localhost:6379 --demo` |
| `src/warmup-before-deploy.sh` | Puerta de despliegue: extraer → calentar críticas+altas → verificar instancia. Sale con error si algo falla. | `REDIS_HOST=redis-new.internal ./src/warmup-before-deploy.sh` |
| `src/k8s-warmup-job.yaml` | `Job` de Kubernetes de un solo disparo que corre el warmup y se limpia solo con `ttlSecondsAfterFinished`. | `kubectl apply -f src/k8s-warmup-job.yaml` |

## Requisitos

- Python 3.10+ y `redis` (`pip install redis`) para los scripts.
- `redis-cli` en el PATH para el paso de verificación de la puerta bash.
- Para extracción con `--lfu`: Redis 4.0+ con `maxmemory-policy` en
  `allkeys-lfu` o `volatile-lfu`. Con políticas LRU el contador de
  frecuencia no existe — usa `--logs` en su lugar.

## Uso

```bash
# 1. Extraer hot keys agrupadas por nivel (críticas/altas/medias/bajas)
python3 src/hot_keys.py --logs /var/log/app/cache-access.jsonl --output hot-keys.json
# o, con una política de expulsión LFU:
python3 src/hot_keys.py --lfu --redis localhost:6379 --output hot-keys.json

# 2. Probar el flujo de warmup contra un Redis local con el loader demo
python3 src/warmup.py --keys hot-keys.json --redis localhost:6379 --demo

# 3. En producción: edita warmup.py, sustituye demo_loader por un loader
#    que lea tu fuente de verdad, y puerta el despliegue:
./src/warmup-before-deploy.sh
```

El runner sale con `0` cuando la cobertura muestreada es ≥ 80% y con `2`
en caso contrario, de modo que un pipeline puede bloquear la conmutación
de tráfico ante un warmup fallido — la misma puerta que describe el runbook.
