# Event Sourcing + CQRS en Python

Implementación ejecutable de una cuenta bancaria event-sourced con separación
CQRS, basada en la receta de StackPractices
[Implementar Event Sourcing con CQRS en Python](https://stackpractices.com/es/recipes/event-sourcing-cqrs-pattern/).

## Qué contiene

| Archivo | Contenido |
| --- | --- |
| `events.py` | Eventos de dominio Pydantic con factories por instancia para `event_id`/`timestamp` y el registro de eventos. |
| `aggregate.py` | Base `AggregateRoot` + `BankAccount` con métodos de comando que validan invariantes y emiten eventos. |
| `event_store.py` | Event store append-only sobre PostgreSQL con concurrencia optimista `UNIQUE(aggregate_id, version)`. |
| `handlers.py` | `CommandHandler`: carga el aggregate, ejecuta el comando y persiste los eventos pendientes. |
| `projectors.py` | `AccountProjector`, `AccountStatsProjector` y `ProjectorManager` con deduplicación durable (`processed_events`). |
| `queries.py` | `AccountQueryService`, lado de lectura sobre las tablas de proyección. |
| `snapshots.py` | `SnapshotStore` + helper `load_aggregate` de snapshot-y-replay. |
| `main.py` | Demo completa: comandos → store → proyecciones → consultas → recarga con snapshot. |

## Ejecutarlo

```bash
pip install -r requirements.txt
export DATABASE_URL=postgresql://user:pass@localhost/eventstore
python main.py
```

Las tablas se crean automáticamente en la primera ejecución (`event_store`,
`snapshots`, `processed_events`, `account_projection`, `transaction_projection`).

## Puntos clave del diseño

- `UNIQUE(aggregate_id, version)` es el guardia real de concurrencia optimista;
  el `SELECT MAX(version)` es solo un camino rápido.
- La deduplicación de proyecciones vive en la tabla `processed_events` y se
  commitea en la misma transacción que la actualización — la idempotencia
  sobrevive a reinicios.
- `metadata` es un nombre reservado en SQLAlchemy Declarative, así que el modelo
  mapea la columna explícitamente como `event_metadata`.
