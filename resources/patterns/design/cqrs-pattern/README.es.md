# Patrón CQRS — Recursos complementarios

Código complementario del [Patrón CQRS](https://stackpractices.com/es/patterns/cqrs-pattern/).

Demos ejecutables de Command Query Responsibility Segregation en tres lenguajes, más una demo de proyección por eventos que muestra la variante asíncrona.

## Contenido

| Archivo | Qué muestra |
| --- | --- |
| `cqrs_demo.py` | Manejador de comandos + manejador de consultas sobre un almacén en memoria, con invariantes en el lado de escritura y un DTO desnormalizado `OrderSummary` en el de lectura. Ejecuta: `python cqrs_demo.py`. |
| `cqrs-demo.js` | La misma división comando/consulta en JavaScript. Ejecuta: `node cqrs-demo.js`. |
| `CqrsDemo.java` | Versión Java tipada con `record Item`, invariante en `Order.confirm()` y un `main` que compila standalone: `javac CqrsDemo.java && java CqrsDemo`. |
| `projection-demo.js` | La variante async: los comandos emiten eventos a un log y un consumidor de proyección reconstruye el modelo de lectura. Demuestra consumidores idempotentes y replay completo (reconstrucción). Ejecuta: `node projection-demo.js`. |

## Cómo usarlo

1. Ejecuta primero las tres demos de almacén único — eso es "CQRS simple".
2. Luego corre `projection-demo.js` para ver cómo eventos + proyecciones reemplazan la sincronía transaccional cuando los almacenes se separan.
3. Experimenta: añade una segunda forma de modelo de lectura a `projection-demo.js` para ver cómo se multiplican las proyecciones — y por qué consolidar importa.
