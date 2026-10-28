# Patrón Blue-Green Deployment — Implementaciones ejecutables

Complemento del patrón de StackPractices [Patrón Blue-Green Deployment](https://stackpractices.com/es/patterns/blue-green-deployment-pattern/).

Simulador de despliegue blue-green en tres implementaciones equivalentes: dos entornos (blue/green), una puerta de smoke tests, conmutación instantánea del tráfico y rollback en un paso a la versión anterior. Solo stdlib — sin dependencias.

## Archivos

| Archivo | Stack | Ejecutar |
| --- | --- | --- |
| `src/blue_green_deployment.py` | Python 3.10+ (solo stdlib) | `python src/blue_green_deployment.py` |
| `src/blue-green-deployment.js` | Node.js 18+ (solo stdlib) | `node src/blue-green-deployment.js` |
| `src/BlueGreenDeployment.java` | Java 10+ (`var`, `Map.of`) | `javac src/BlueGreenDeployment.java && java -cp src BlueGreenDeployment` |

Cada ejecución despliega la v2.0.0 en el entorno inactivo, corre dos smoke tests, conmuta el tráfico y luego simula un problema para hacer rollback — imprimiendo el estado y el historial de despliegues en cada paso. Haz que un smoke test devuelva `false` para ver el camino de despliegue fallido.
