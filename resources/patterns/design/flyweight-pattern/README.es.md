# Patrón Flyweight: Objetos Compartidos para Memoria

Código companion para el [recurso del patrón Flyweight](https://stackpractices.com/es/patterns/flyweight-pattern/) en StackPractices.

## Archivos

| Archivo | Descripción |
| --- | --- |
| `flyweight_python.py` | Implementación en Python con cache WeakValueDictionary |
| `flyweight_javascript.js` | Implementación en JavaScript con cache Map |
| `FlyweightJava.java` | Implementación en Java con ConcurrentHashMap |
| `test_flyweight.py` | Tests unitarios para la implementación en Python (pytest) |

## Setup

```bash
pip install pytest
```

## Ejecutar los ejemplos

```bash
python flyweight_python.py
node flyweight_javascript.js
javac FlyweightJava.java && java FlyweightJava
```

## Ejecutar los tests

```bash
python -m pytest test_flyweight.py -v
```

## Uso

```python
from flyweight_python import TreeType, Tree, build_forest

forest = build_forest(1000)
for tree in forest:
    print(tree.render())
print(f"Tipos únicos: {TreeType.cache_size()}")
```
