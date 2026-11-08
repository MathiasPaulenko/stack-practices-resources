# Deep Clone Strategies — Runnable Implementations

Companion to the StackPractices recipe [Deep Clone Objects in JavaScript: Beyond JSON.parse](https://stackpractices.com/recipes/deep-clone-structured/).

A deep clone comparison in three languages: a JSON round-trip that silently degrades types (dates become strings, sets become empty objects, circular references throw) versus a proper deep clone that preserves everything. Stdlib only — no dependencies needed.

## Files

| File | Stack | Run |
| --- | --- | --- |
| `src/deep_clone.py` | Python 3.9+ (stdlib only) | `python src/deep_clone.py` |
| `src/deep-clone.js` | Node.js 17+ (`structuredClone`) | `node src/deep-clone.js` |
| `src/DeepClone.java` | Java 11+ | `javac -d src src/DeepClone.java && java -cp src DeepClone` |

Each run shows the same scenario: an object with a `Date`/`Instant`, a `Set`, a nested structure, and a circular or child reference. The JSON path fails or loses types; the native deep clone (`copy.deepcopy`, `structuredClone`, copy constructor) keeps every type and produces fully independent copies.

Java has no `structuredClone` equivalent in the JDK; the idiomatic deep clone is a copy constructor or a library (`SerializationUtils.clone`, MapStruct). Python's `copy.deepcopy` is the closest built-in equivalent and handles cycles out of the box.
