# Patrón Composite — Recursos Complementarios

Ejemplos ejecutables de la guía del [Patrón Composite](https://stackpractices.com/es/patterns/composite-pattern/) en StackPractices.

## Archivos

| Archivo | Qué muestra |
|---|---|
| `file_system.py` | Árbol compuesto File/Folder en Python — ejecútalo con `python file_system.py` |
| `file-system.js` | El mismo ejemplo en JavaScript — `node file-system.js` |
| `FileSystem.java` | El mismo ejemplo en Java — `javac FileSystem.java && java FileSystem` |
| `expression-tree.ts` | Segundo dominio: árbol de expresiones aritméticas con `eval()` — `npx tsx expression-tree.ts` |
| `test_cycle_check.py` | `add()` seguro que rechaza ciclos + suite unittest — `python test_cycle_check.py` |

## Notas

- Los ejemplos del sistema de archivos usan la variante **segura**: `add()`/`remove()` existen solo en `Folder`, no en la interfaz compartida.
- `test_cycle_check.py` demuestra el chequeo de ancestros descrito en el FAQ — insertar una carpeta dentro de su propio subárbol lanza `ValueError`.
- El árbol de expresiones muestra por qué el patrón generaliza más allá de contenedores: operadores y números comparten `eval()`.

Artículo original (ES): <https://stackpractices.com/es/patterns/composite-pattern/>
