# Companion de Traffic Mirroring

Configs ejecutables para mirroring de tráfico con Nginx, Istio, Envoy y GoReplay.

## Archivos

| Archivo | Descripción |
|---------|-------------|
| `nginx.conf` | Config del módulo Nginx mirror con filtrado de health checks y assets |
| `istio-virtualservice.yaml` | VirtualService + DestinationRule de Istio para 10% mirroring |
| `envoy.yaml` | Config estática de Envoy con request mirror policy al 10% |
| `goreplay-commands.sh` | Comandos CLI de GoReplay para captura, replay y filtrado |
| `response_comparison.js` | Middleware Express que mirror tráfico y differea respuestas |
| `test_mirror.py` | Tests pytest para conectividad, idempotencia, schema, auth, latencia |
| `docker-compose.yml` | Docker Compose con Nginx producción + staging + GoReplay |

## Inicio Rápido

```bash
# Levantar producción y staging con Nginx mirror
docker-compose up -d

# Correr tests
pip install -r requirements.txt
pytest test_mirror.py -v
```

## Recurso Relacionado

[Traffic Mirroring para Testing en Producción](https://stackpractices.com/es/recipes/traffic-mirroring/)
