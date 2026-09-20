# Patrón Prototype — Recursos Companion

Ejemplos ejecutables del [patrón Prototype](https://stackpractices.com/es/patterns/prototype-pattern/) en StackPractices.

El patrón estampa objetos nuevos copiando una instancia configurada en lugar de reconstruirla desde cero. Ambas implementaciones incluyen un `PrototypeRegistry`: un mapa de prototipos con nombre que devuelve un clon independiente en cada `get()`.

## Archivos

| Archivo | Qué muestra |
|---------|-------------|
| `prototype.py` | Prototipo `ProductConfig` + `PrototypeRegistry` en Python — `copy.deepcopy` para independencia de estructuras anidadas |
| `test_prototype.py` | Suite pytest: 6 tests cubriendo identidad del clon, independencia de copia profunda, aislamiento del registro, claves desconocidas y rechazo de no clonables |
| `prototype.js` | El mismo registro en JavaScript — un `clone()` *manual* que conserva la clase (con comentario de por qué `structuredClone` no lo hace) |
| `prototype.test.js` | Suite `node:test`: 7 tests incluyendo el caso de conservación de `instanceof` |

## Ejecutar

```bash
# Demo + tests Python
python prototype.py
python -m pytest test_prototype.py -v

# Demo + tests JavaScript (Node 18+)
node prototype.js
node --test prototype.test.js
```

## Ideas clave

- La copia profunda es lo que hace a los clones independientes — `attributes`/`tags` anidados se duplican, así mutar un clon nunca toca el prototipo.
- `structuredClone` copia los datos pero pierde la cadena de prototipos; el ejemplo JS clona a mano para conservar `instanceof` y los métodos.
- Los prototipos registrados se tratan como de solo lectura: los llamadores siempre trabajan sobre clones.
- Clonar supera a construir solo cuando la inicialización es cara (parseo, I/O, cableado del grafo) — para asignación de campos simple, el constructor es más rápido.

CI: `.github/workflows/test.yml` ejecuta ambas suites de tests en cada cambio a esta carpeta.
