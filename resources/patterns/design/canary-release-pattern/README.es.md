# Patrón Canary Release — Implementaciones ejecutables

Complemento del patrón de StackPractices [Patrón Canary Release](https://stackpractices.com/es/patterns/canary-release-pattern/).

Un simulador de canary release en tres implementaciones equivalentes: lista de etapas (1 % → 5 % → 25 % → 50 % → 100 %), una puerta de métricas de salud tras cada bake, rollback automático en la primera etapa que falla y promoción cuando el canary llega al 100 %. Solo stdlib — sin dependencias.

## Archivos

| Archivo | Stack | Ejecutar |
| --- | --- | --- |
| `src/canary_release.py` | Python 3.9+ (solo stdlib) | `python src/canary_release.py` |
| `src/canary-release.js` | Node.js 14+ (solo stdlib) | `node src/canary-release.js` |
| `src/CanaryRelease.java` | Java 16+ (`record`, `var`, `Map.of`) | `javac src/CanaryRelease.java && java -cp src CanaryRelease` |

Cada ejecución avanza por las etapas y evalúa un health check simulado que devuelve métricas degradadas en la tercera llamada, así que verás el camino de rollback de principio a fin. Edita `mock_health_check`/`mockHealthCheck` para que siempre devuelva métricas sanas y obtendrás el camino de promoción completa.

Los bake times son fracciones de segundo para que la demo termine al instante; en producción cada etapa dura 5-30 minutos contra métricas reales (Prometheus, Datadog, etc.).
