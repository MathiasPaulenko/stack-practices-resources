# Domain-Driven Design (DDD) Companion

Implementations of DDD building blocks: entities, value objects, aggregates, repositories, domain events, and anti-corruption layers with tests.

## Files

| File | Language | Description |
|------|----------|-------------|
| `python_entities_value_objects.py` | Python | Entities, value objects (Money, Address), OrderLine, Order with invariants |
| `python_aggregate_root.py` | Python | Aggregate root with invariant enforcement and domain events |
| `python_repositories_events.py` | Python | Repository pattern (in-memory), event dispatcher, event handlers |
| `java_order_aggregate.java` | Java | Order aggregate root with Money value object and invariants |
| `java_anti_corruption_layer.java` | Java | Anti-Corruption Layer (ACL) between Sales and Inventory contexts |
| `test_aggregates.py` | Python | pytest tests for aggregate invariants (8 tests) |
| `test_value_objects.py` | Python | pytest tests for value object equality and immutability (10 tests) |
| `test_domain_events.py` | Python | pytest tests for repository and event dispatcher (4 tests) |

## Quick Start

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

## Key Concepts Demonstrated

- **Value objects**: Money and Address (immutable, compared by value)
- **Entities**: Order and OrderLine (have identity, mutable state)
- **Aggregate root**: Order controls all modifications, enforces invariants
- **Domain events**: OrderConfirmed published on confirmation
- **Repository**: In-memory implementation of OrderRepository
- **Event dispatcher**: Subscribe and publish domain events
- **Anti-Corruption Layer**: Translates between bounded contexts
- **Invariants**: Cannot modify confirmed order, max 50 items, positive quantity
