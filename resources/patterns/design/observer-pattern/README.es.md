# Patrón Observer — Recursos Complementarios

Implementaciones ejecutables del patrón Observer de la [guía de StackPractices](https://stackpractices.com/es/patterns/observer-pattern/):

| Archivo | Lenguaje | Qué muestra |
|---------|----------|-------------|
| `observer.py` | Python 3 | Subject con attach/notify y callables de desuscripción |
| `observer.js` | JavaScript | Lista de observadores con `Set`, aislamiento de errores |
| `Subject.java` | Java | Interfaz `Observer` tipada, desuscripción con `Runnable` |
| `event-emitter.ts` | TypeScript | Canales por evento con `Map<string, Set<Observer>>` |

Cada `subscribe`/`attach` devuelve un manejador de desuscripción — llámalo en el teardown para evitar la fuga de memoria clásica. Cada `notify`/`emit` envuelve las llamadas para que un observador que falla no rompa al resto.

## Ejecutar

```bash
python observer.py
node observer.js
javac Subject.java && java Subject
npx tsx event-emitter.ts   # o ts-node
```
