# Patrón de Convoy Secuencial — Recursos companion

Implementaciones ejecutables del Patrón de Convoy Secuencial en Python, Java y
JavaScript. Cada una simula un broker particionado en memoria, así que corren
sin Kafka, Service Bus ni Redis.

## Archivos

| Archivo | Lenguaje | Descripción |
|---------|----------|-------------|
| `convoy_processor.py` | Python | Router de particiones, sequence numbers por entidad, consumidor ordenado con buffer de gaps |
| `ConvoyProcessor.java` | Java | La misma simulación: `PartitionedBroker`, `ConvoyProducer`, `ConvoyConsumer` |
| `convoy_processor.js` | JavaScript | La misma simulación con `Map` para secuencias y métodos privados |

## Ejecutar los ejemplos

```bash
python convoy_processor.py
javac ConvoyProcessor.java && java ConvoyProcessor
node convoy_processor.js
```

Cada script produce tres eventos para `user-123`, los entrega desordenados
(la secuencia 3 antes que la 2) y verifica que el consumidor los aplica en orden.

## Conceptos clave

- **Partition key**: los eventos de la misma entidad caen en la misma
  partición, así un solo consumidor los posee.
- **Sequence numbers**: el productor adjunta un contador por entidad; el
  consumidor lo usa para detectar gaps y duplicados.
- **Buffer de gaps**: los eventos desordenados esperan en un buffer por
  entidad hasta que llegan las secuencias faltantes.

## Fuente

Companion del artículo de StackPractices:
<https://stackpractices.com/es/patterns/sequential-convoy-pattern/>
