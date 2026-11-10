# Patrón Event Bus — Archivos complementarios

Event bus en memoria ejecutable para el patrón en
[stackpractices.com](https://stackpractices.com/es/patterns/event-bus-pattern/).

## Archivos

- `event_bus.py` — Python: bus thread-safe (`threading.Lock`), `subscribe()` devuelve una función de desuscripción, aislamiento de excepciones por handler
- `test_event_bus.py` — pytest: fan-out, desuscripción, filtrado por tipo, aislamiento de fallos, desuscripción durante el dispatch
- `event_bus.js` — JavaScript: bus basado en `Map` con funciones de desuscripción (Node 18+, ESM)
- `event_bus.test.js` — suite `node:test` que refleja los tests de Python
- `EventBus.java` — Java: evento `record` + `CopyOnWriteArrayList` para dispatch sin locks, `main` incluido

## Inicio rápido

```bash
python event_bus.py          # solo stdlib
pytest test_event_bus.py -q  # 5 tests
node event_bus.js            # Node 18+
node --test event_bus.test.js
javac EventBus.java && java EventBus
```

Cada demo publica `UserRegistered` dos veces — antes y después de que un
suscriptor se desuscriba — para ver el fan-out y la limpieza en acción.
