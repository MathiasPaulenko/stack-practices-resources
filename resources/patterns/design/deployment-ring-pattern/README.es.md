# Patrón Deployment Ring — Implementaciones ejecutables

Código companion del patrón de StackPractices:
[Patrón Deployment Ring](https://stackpractices.com/es/patterns/deployment-ring-pattern/)

Despliegue progresivo por anillos de tamaño creciente (1% → 5% → 25% → 100%)
con una puerta de salud entre cada etapa. Si un anillo falla su puerta, se
revierten todos los anillos completados, no solo el que falló.

## Archivos

| Archivo | Qué muestra |
|---------|-------------|
| `src/ring_deployment.py` | Desplegador por anillos en Python con dataclasses, máquina de estados enum y rollback |
| `src/ring-deployment.js` | La misma lógica en JavaScript asíncrono |
| `src/RingDeployment.java` | Versión con records de Java 16+ |
| `ring-config.yaml` | Configuración de anillos de ejemplo: audiencias, ventanas de bake, umbrales de la puerta de salud, política de rollback |

## Ejecutar

```bash
python src/ring_deployment.py     # Python 3.8+
node src/ring-deployment.js       # Node 14+
javac src/RingDeployment.java && java -cp src RingDeployment   # Java 16+
```

Los tres ejecutan el mismo escenario: un health check simulado falla en la
tercera llamada (anillo 2 al 25%), así que los anillos 0–1 se completan y
después se revierten. Salida final esperada:

```text
FAIL - Ring 2 failed health check, rolling back
  Rolling back ring 1 (early-adopters)
  Rolling back ring 0 (internal)

Result: {'version': '2.1.0', 'status': 'rolled_back', 'failed_ring': 2, 'rings_completed': 2}
```

## Conectarlo a un sistema real

Sustituye `mock_health_check` por una llamada a tu backend de métricas
(Prometheus, Datadog, CloudWatch) y enruta los porcentajes de anillo con
feature flags, pesos del balanceador o tu service mesh. El archivo
`ring-config.yaml` refleja los parámetros que exponen las implementaciones.
