# Patrón Marker Interface — Recursos complementarios

Código complementario del patrón [Marker Interface](https://stackpractices.com/es/patterns/marker-interface-pattern/).

Demos ejecutables del patrón en tres lenguajes, cada una mostrando la misma idea — una etiqueta de tipo vacía más un check en runtime — implementada con el mecanismo propio de cada lenguaje.

## Contenido

| Archivo | Qué muestra |
| --- | --- |
| `marker_demo.py` | Clases base `ABC` vacías como markers + checks de `isinstance`. Incluye la prueba de que el check discrimina (`User` vs `SerializableUser`). Nota: un `Protocol` vacío coincidiría con todo — ver el docstring del módulo. |
| `MarkerDemo.java` | Marker interfaces propias (`Auditable`, `Immutable`) con checks de `instanceof`. Compila y corre standalone: `javac MarkerDemo.java && java MarkerDemo`. |
| `marker-demo.js` | Claves `Symbol` como markers en los constructores + checks estáticos. Ejecuta: `node marker-demo.js`. |

## Cómo usarlo

1. Ejecuta cada demo y confirma que la clase marcada pasa y la sin marcar es rechazada.
2. Prueba marcar `SecretData`/`MutableConfig` y observa cómo cambian los checks.
3. Compara mecanismos: clase base (Python), interfaz (Java), symbol (JS) — mismo patrón, maquinaria distinta.
