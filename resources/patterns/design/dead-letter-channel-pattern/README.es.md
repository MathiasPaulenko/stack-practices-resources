# Patrón Dead Letter Channel — Implementaciones ejecutables

Recurso auxiliar del patrón [Patrón Dead Letter Channel](https://stackpractices.com/es/patterns/dead-letter-channel-pattern/) de StackPractices.

Una demo de dead letter channel en tres implementaciones equivalentes: un broker en memoria con cola principal, cola de reintento y cola de mensajes muertos (DLQ). El consumidor procesa pedidos; un mensaje llega sin `order_id` (un mensaje tóxico), falla en cada intento, agota su presupuesto de 3 reintentos y aterriza en la DLQ con los metadatos del fallo. Solo stdlib — sin dependencias.

## Archivos

| Archivo | Stack | Ejecutar |
| --- | --- | --- |
| `src/dead_letter_channel.py` | Python 3.9+ (solo stdlib) | `python src/dead_letter_channel.py` |
| `src/dead-letter-channel.js` | Node.js 14+ (solo stdlib) | `node src/dead-letter-channel.js` |
| `src/DeadLetterChannel.java` | Java 16+ (`record`) | `javac src/DeadLetterChannel.java && java -cp src DeadLetterChannel` |

Cada ejecución muestra los dos pedidos sanos procesándose, el mensaje tóxico reintentando y moviéndose a la DLQ, las profundidades finales de las colas y un paso de reprocesamiento que repara el payload y lo vuelve a encolar.

El broker aquí es un stub en memoria para que la demo corra en cualquier sitio; en producción cambiarías `Broker` por SQS (redrive policy), RabbitMQ (dead letter exchange) o un topic de errores de Kafka — la lógica de reintento/DLQ/reproceso es idéntica.
