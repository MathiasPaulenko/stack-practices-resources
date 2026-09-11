# Flyweight Pattern: Shared Objects for Memory Efficiency

Companion code for the [Flyweight pattern resource](https://stackpractices.com/patterns/flyweight-pattern/) on StackPractices.

## Files

| File | Description |
| --- | --- |
| `flyweight_python.py` | Python implementation with WeakValueDictionary cache |
| `flyweight_javascript.js` | JavaScript implementation with Map cache |
| `FlyweightJava.java` | Java implementation with ConcurrentHashMap |
| `test_flyweight.py` | Unit tests for the Python implementation (pytest) |

## Setup

```bash
pip install pytest
```

## Running the Examples

```bash
python flyweight_python.py
node flyweight_javascript.js
javac FlyweightJava.java && java FlyweightJava
```

## Running the Tests

```bash
python -m pytest test_flyweight.py -v
```

## Usage

```python
from flyweight_python import TreeType, Tree, build_forest

forest = build_forest(1000)
for tree in forest:
    print(tree.render())
print(f"Unique types: {TreeType.cache_size()}")
```
