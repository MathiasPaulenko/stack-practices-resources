# Patrón Claim Check — Implementaciones ejecutables

Companion del patrón de StackPractices [Patrón Claim Check](https://stackpractices.com/es/patterns/claim-check-pattern/).

Una demo de claim check en tres implementaciones equivalentes: un blob store en memoria que simula S3/Azure Blob/GCS, un broker de mensajes mínimo y una pareja productor/consumidor. El productor almacena un reporte de 1MB+ en el storage, publica solo el token de claim en el broker, y el consumidor descarga el payload por token y lo elimina tras procesarlo. Solo stdlib — sin dependencias.

## Archivos

| Archivo | Stack | Ejecutar |
| --- | --- | --- |
| `src/claim_check.py` | Python 3.9+ (solo stdlib) | `python src/claim_check.py` |
| `src/claim-check.js` | Node.js 14+ (solo stdlib) | `node src/claim-check.js` |
| `src/ClaimCheck.java` | Java 15+ (`text blocks`, `Map.of`) | `javac src/ClaimCheck.java && java -cp src ClaimCheck` |

Cada ejecución imprime el token de claim, el tamaño del payload que viajó por el broker (unos pocos cientos de bytes en lugar de 1MB+), la recuperación y la eliminación. Para ver el camino de fallo, elimina el token del storage antes de que corra el consumidor — el consumidor loguea `Claim check ... no encontrado` en lugar de romperse, que es el manejo de errores que necesita un consumidor real.

El broker y el storage son stubs en memoria para que la demo corra en cualquier parte; en producción cambiarías `BlobStorage` por un cliente de S3/Azure Blob/GCS y `MessageBroker` por SQS, Kafka o RabbitMQ — la lógica de claim check queda idéntica.
