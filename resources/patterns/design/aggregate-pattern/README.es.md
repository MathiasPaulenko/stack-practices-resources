# Patrón Aggregate — Companion

Ejemplos ejecutables del Patrón Aggregate de [StackPractices](https://stackpractices.com/es/patterns/aggregate-pattern/).

La clase `Order` actúa como aggregate root. Protege la invariante de que un pedido enviado debe tener al menos una línea, e impide modificaciones después del envío.

## Archivos

- `src/aggregate_pattern.py` — versión Python con dataclasses
- `src/aggregate-pattern.js` — versión JavaScript con clases
- `src/Aggregate.java` — versión Java con `record`

## Ejecutar

```bash
python src/aggregate_pattern.py
node src/aggregate-pattern.js
javac src/Aggregate.java && java -cp src Order
```
