# Patrón Domain Event — Archivos complementarios

Ejemplos ejecutables para el patrón en
[stackpractices.com](https://stackpractices.com/es/patterns/domain-event-pattern/).

## Archivos

- `domain_events.py` — Python: evento como dataclass frozen + aggregate `Order` + `EventPublisher` de clase con dos suscriptores reales
- `domain_events.js` — JavaScript: mismo modelo con `crypto.randomUUID()` (Node 19+)
- `DomainEvents.java` — Java: evento `record` + publisher `Consumer<DomainEvent>`, con `main` incluido

## Inicio rápido

```bash
python domain_events.py   # solo stdlib
node domain_events.js     # Node 19+
javac DomainEvents.java && java DomainEvents
```

Cada script crea un pedido, lo envía, drena `clearEvents()` y publica — verás cómo reaccionan los handlers de email y analíticas.
