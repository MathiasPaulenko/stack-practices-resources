# Contenedor de Dependency Injection — Implementaciones ejecutables

Companion del patrón de StackPractices [Contenedor de Dependency Injection en TypeScript](https://stackpractices.com/es/patterns/dependency-injection-typescript/).

Un contenedor DI mínimo en tres lenguajes: los servicios registran una factory bajo un token y el contenedor resuelve el grafo de dependencias de forma perezosa. Se demuestran tres lifetimes — singleton (una instancia compartida), transient (nueva por resolve) y scoped (una instancia por scope de request). Solo stdlib, sin dependencias.

## Archivos

| Archivo | Stack | Ejecutar |
| --- | --- | --- |
| `src/di-container.js` | Node.js 18+ | `node src/di-container.js` |
| `src/di_container.py` | Python 3.10+ | `python src/di_container.py` |
| `src/DiContainer.java` | Java 11+ | `javac -d src src/DiContainer.java && java -cp src DiContainer` |

Cada ejecución conecta el mismo grafo — `UserService` → `UserRepository` → `Database` + `Logger` — y verifica la semántica de lifetimes: el singleton se comparte entre la raíz y todos los scopes, los transients son objetos nuevos, y cada scope guarda sus propias copias.

El archivo JavaScript es un port directo del contenedor TypeScript del artículo (devuélvele los tipos para producción). Python y Java muestran la misma idea sin decoradores: la factory es el cableado y la inyección ocurre solo en el composition root.
