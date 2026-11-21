# Memento Pattern — Companion Resources

Companion code for the [Memento Pattern](https://stackpractices.com/patterns/memento-pattern/) on StackPractices: the Originator/Memento/Caretaker split as a text editor undo stack, in three languages.

## Files

| File | Language | Description |
| --- | --- | --- |
| `src/memento_pattern.py` | Python 3.10+ | `TextEditor` originator, opaque `EditorMemento`, bounded `History` caretaker |
| `src/mementoPattern.js` | JavaScript (Node 18+) | Same design; snapshots frozen with `Object.freeze` |
| `src/MementoDemo.java` | Java 11+ | Same design; package-private memento getters keep state opaque |

All versions include schema versioning on the snapshot and mid-text insertion that preserves the tail (a common bug in naive `type()` implementations).

## Quick start

```bash
python src/memento_pattern.py     # demo: type/undo/mid-text insert
node src/mementoPattern.js        # same demo
javac src/MementoDemo.java -d out && java -cp out MementoDemo
```

No dependencies beyond the language runtimes.
