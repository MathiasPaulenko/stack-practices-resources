# Patrón Module — Ejemplos Complementarios

Ejemplos ejecutables del [Patrón Module](https://stackpractices.com/es/patterns/module-pattern/) de StackPractices.

## Contenido

| Archivo | Variante | Ejecutar |
|---------|----------|----------|
| `iife-counter.js` | Closure IIFE (estilo pre-ES6) | `node iife-counter.js` |
| `esm-counter.js` + `esm-main.js` | ES module | `node esm-main.js` |
| `counter.py` | Módulo Python (convención `_privado`) | `python counter.py` |
| `Counter.java` | Clase estática Java | `javac Counter.java && java com.myapp.counter.Counter` |
| `payment-module.ts` | Escenario de pagos con ciclo de vida y estado privado | `npx tsx payment-module.ts` |

## Notas

- Cada variante mantiene `count`/`log` privados y expone solo `increment`, `decrement`, `getCount` — mismo contrato, cuatro mecanismos.
- El estado del módulo es estado compartido: cada importer ve el mismo `count`. Para instancias independientes hace falta una factory o una clase, no un módulo.
- Migrar una IIFE a un ES module: sube el cuerpo al nivel superior, elimina la envoltura y reemplaza el objeto retornado con `export`s.

## Relacionado

- [Patrón Singleton](https://stackpractices.com/es/patterns/singleton-pattern/)
- [Patrón Facade](https://stackpractices.com/es/patterns/facade-pattern/)
