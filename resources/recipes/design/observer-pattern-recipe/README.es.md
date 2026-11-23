# Observer Pattern — Recursos complementarios

Versiones ejecutables de las implementaciones del observer pattern de la
[receta Observer Pattern](https://stackpractices.com/es/recipes/observer-pattern-recipe/)
en StackPractices.

## Archivos

| Archivo | Qué muestra |
| --- | --- |
| `order-event-emitter.ts` | Event emitter tipado básico para eventos del ciclo de vida de pedidos (Node.js/TypeScript) |
| `typed-event-emitter.ts` | Emitter con seguridad de tipos en compilación mediante un mapa de eventos y aislamiento de errores por listener |
| `debounced-event-emitter.ts` | Emitter que agrupa eventos de alta frecuencia (p. ej., pulsaciones de tecla) en una sola notificación |
| `weak-observer.ts` | Registro de observers basado en `WeakRef` para que el GC pueda recolectar los targets |
| `order-observer.java` | Observer con `PropertyChangeSupport`, el mecanismo integrado del JDK |
| `reactive-orders.py` | Reactive streams con RxPY: subject, suscripciones filtradas y mapeadas |

## Ejecución

Los archivos TypeScript se ejecutan con `ts-node`, `tsx` o tras compilar con `tsc`:

```bash
npx tsx order-event-emitter.ts
```

Java necesita un JDK (11+):

```bash
javac order-observer.java && java OrderObserverDemo
```

Python necesita RxPY:

```bash
pip install reactivex
python reactive-orders.py
```
