# Companion de Domain-Driven Design (DDD)

Implementaciones de los building blocks de DDD: entidades, value objects, aggregates, repositorios, domain events y anti-corruption layers con tests.

## Archivos

| Archivo | Lenguaje | Descripción |
|---------|----------|-------------|
| `python_entities_value_objects.py` | Python | Entidades, value objects (Money, Address), OrderLine, Order con invariantes |
| `python_aggregate_root.py` | Python | Aggregate root con enforcement de invariantes y domain events |
| `python_repositories_events.py` | Python | Patrón repository (in-memory), event dispatcher, event handlers |
| `java_order_aggregate.java` | Java | Order aggregate root con Money value object e invariantes |
| `java_anti_corruption_layer.java` | Java | Anti-Corruption Layer (ACL) entre contexts de Sales e Inventory |
| `test_aggregates.py` | Python | Tests pytest para invariantes del aggregate (8 tests) |
| `test_value_objects.py` | Python | Tests pytest para igualdad e inmutabilidad de value objects (10 tests) |
| `test_domain_events.py` | Python | Tests pytest para repository y event dispatcher (4 tests) |

## Inicio Rápido

### Python

```bash
pip install -r requirements.txt
python python_entities_value_objects.py
python python_aggregate_root.py
python python_repositories_events.py
pytest test_aggregates.py test_value_objects.py test_domain_events.py -v
```

### Java

```bash
javac java_order_aggregate.java
java OrderDemo

javac java_anti_corruption_layer.java
java ACLDemo
```

## Conceptos Clave Demostrados

- **Value objects**: Money y Address (inmutables, comparados por valor)
- **Entidades**: Order y OrderLine (tienen identidad, estado mutable)
- **Aggregate root**: Order controla todas las modificaciones, enforce invariantes
- **Domain events**: OrderConfirmed publicado al confirmar
- **Repository**: Implementación in-memory de OrderRepository
- **Event dispatcher**: Suscribir y publicar domain events
- **Anti-Corruption Layer**: Traduce entre bounded contexts
- **Invariantes**: No modificar orden confirmada, máx 50 items, cantidad positiva
