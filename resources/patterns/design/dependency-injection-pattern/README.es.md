# Patrón Dependency Injection — Código complementario

Ejemplos ejecutables que acompañan al recurso
[Patrón Dependency Injection](https://stackpractices.com/es/patterns/dependency-injection-pattern/)
en StackPractices.

## Archivos

| Archivo | Descripción |
|---------|-------------|
| `dependency_injection.py` | `OrderService` recibe `PaymentProcessor` + `Logger` por constructor — cableado manual en `composition_root()` más un `Container` mínimo con scope singleton |
| `dependency-injection.ts` | La misma forma en TypeScript — `Container` tipado usando clases abstractas como tokens de inyección |

## Requisitos

- Python 3.9+ — sin dependencias, corre con `python dependency_injection.py`
- TypeScript — corre con `npx tsx dependency-injection.ts` o `ts-node`

## Notas

- El contenedor es una herramienta didáctica (~30 líneas): en proyectos
  reales usa tsyringe, InversifyJS, Spring o lo que tu framework provea.
- Fíjate en el modo de fallo: `resolve()` sobre un token no registrado
  lanza error — ese es el error de cableado en runtime que DI cambia
  por flexibilidad.
- El registro singleton muestra de dónde vienen los bugs de estado por
  request: un `Logger` singleton está bien, una dependencia por-request no.
