# Patrón Event-Carried State Transfer — Implementaciones ejecutables

Companion del patrón de StackPractices [Patrón Event-Carried State Transfer](https://stackpractices.com/es/patterns/event-carried-state-transfer-pattern/).

Una demo de ECST en tres implementaciones equivalentes: un `CustomerService` que posee los datos de clientes, un bus de eventos en memoria que hace las veces de Kafka, y un consumidor `OrderService` que aplica cada evento de state transfer a una réplica local y sirve lecturas sin llamar al origen. Cada evento lleva el estado completo de la entidad más un número de secuencia `version`, para que los consumidores detecten entregas desordenadas o duplicadas. Solo stdlib — sin dependencias.

## Archivos

| Archivo | Stack | Ejecutar |
| --- | --- | --- |
| `src/ecst.py` | Python 3.9+ (solo stdlib) | `python src/ecst.py` |
| `src/ecst.js` | Node.js 14+ (solo stdlib) | `node src/ecst.js` |
| `src/EventCarriedStateTransfer.java` | Java 16+ (`record`, `var`) | `javac src/EventCarriedStateTransfer.java && java -cp src EventCarriedStateTransfer` |

Cada ejecución imprime el log de replicación: el evento de creación del cliente, la lectura local servida desde la réplica, el evento de actualización de tier y la copia local actualizada. En producción cambiarías el `EventBus` en memoria por un topic de Kafka (el artículo muestra la variante con Spring Cloud Stream) y la réplica `Map`/tabla SQLite por el store que ya use el consumidor — la lógica de aplicar-y-leer queda idéntica.
