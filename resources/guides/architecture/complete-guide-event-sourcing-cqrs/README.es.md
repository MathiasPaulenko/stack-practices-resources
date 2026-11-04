# Event Sourcing y CQRS — Assets del ejemplo

Piezas ejecutables de
[Event Sourcing y CQRS: Event Store, Proyecciones](https://stackpractices.com/es/guides/complete-guide-event-sourcing-cqrs/).

## Contenido

| Archivo | Qué muestra |
| --- | --- |
| `event-store-schema.sql` | Tablas `events` + `snapshots` con `UNIQUE(stream_id, version)` |
| `EventStore.ts` | Store append-only con optimistic concurrency |
| `OrderAggregate.ts` | Aggregate root: `raise`/`apply`/`loadFromHistory` |
| `OrderProjection.ts` | Constructor del read model suscrito a eventos |
| `SnapshotStore.ts` | Guardado/carga de snapshots para evitar replays largos |

## Uso

Los archivos son la implementación de referencia — combínalos en tu app o adáptalos a EventStoreDB/Axon para mayor throughput.
