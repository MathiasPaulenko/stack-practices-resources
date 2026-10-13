# Patrón Saga — Archivos complementarios

Implementaciones ejecutables de saga orquestada en tres lenguajes. Cada una
corre el mismo flujo de reserva de viaje del artículo — reservar vuelo, reservar
hotel, cobrar el pago — donde el paso de pago siempre falla para que puedas ver
las transacciones compensatorias deshaciendo los pasos completados en orden
inverso.

Artículo origen: <https://stackpractices.com/es/patterns/saga-pattern/>

## Archivos

| Archivo | Lenguaje | Notas |
|---------|----------|-------|
| `saga_orchestrator.py` | Python 3.8+ | `SagaOrchestrator` guarda los pasos completados y los recorre hacia atrás ejecutando `compensation` ante un fallo |
| `sagaOrchestrator.mjs` | Node.js 18+ | `execute`/`rollback` async, soporta acciones y compensaciones asíncronas |
| `SagaOrchestrator.java` | Java 11+ | pasos basados en `Consumer`; `main` corre la demo de reserva |

## Ejecutar

```bash
python saga_orchestrator.py            # sin dependencias
node sagaOrchestrator.mjs              # sin dependencias
javac SagaOrchestrator.java && java SagaOrchestrator
```

Cada demo imprime el camino feliz de `reserve_flight` y `reserve_hotel`, luego
el fallo de `charge_payment` y las compensaciones corriendo en reversa
(`cancelHotel` → `cancelFlight`).

## Para producción

Una lista de pasos en memoria lo pierde todo si el proceso muere a media saga.
En producción quieres un log de saga persistido y timeouts por paso — o un
framework que te dé ambos:

- **Temporal / Cadence**: workflows durables con manejadores de compensación
- **Axon Framework, Eventuate Tram** (Java): orquestación de sagas sobre mensajería
- **MassTransit** (.NET): máquinas de estado de saga con correlación de mensajes
- **AWS Step Functions**: los bloques `Catch` actúan como compensaciones
