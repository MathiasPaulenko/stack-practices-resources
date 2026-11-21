# Patrón Memento — Recursos Companion

Código companion del [Patrón Memento](https://stackpractices.com/es/patterns/memento-pattern/) en StackPractices: la separación Originator/Memento/Caretaker como pila de deshacer de un editor de texto, en tres lenguajes.

## Archivos

| Archivo | Lenguaje | Descripción |
| --- | --- | --- |
| `src/memento_pattern.py` | Python 3.10+ | `TextEditor` originator, `EditorMemento` opaco, caretaker `History` acotado |
| `src/mementoPattern.js` | JavaScript (Node 18+) | Mismo diseño; instantáneas congeladas con `Object.freeze` |
| `src/MementoDemo.java` | Java 11+ | Mismo diseño; getters package-private mantienen el estado opaco |

Todas las versiones incluyen versionado de esquema en la instantánea e inserción a mitad de texto que conserva el resto (un bug común en implementaciones ingenuas de `type()`).

## Inicio rápido

```bash
python src/memento_pattern.py     # demo: escribir/deshacer/inserción a mitad
node src/mementoPattern.js        # misma demo
javac src/MementoDemo.java -d out && java -cp out MementoDemo
```

Sin dependencias más allá de los runtimes de cada lenguaje.
