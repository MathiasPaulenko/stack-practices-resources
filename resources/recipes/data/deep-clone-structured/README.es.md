# Estrategias de deep clone — Implementaciones ejecutables

Companion de la receta de StackPractices [Deep Clone de Objetos en JavaScript: Más Allá de JSON.parse](https://stackpractices.com/es/recipes/deep-clone-structured/).

Una comparación de deep clone en tres lenguajes: un round-trip JSON que degrada tipos en silencio (las fechas se vuelven strings, los sets se vuelven objetos vacíos, las referencias circulares lanzan error) frente a un clonado profundo real que lo preserva todo. Solo stdlib — sin dependencias.

## Archivos

| Archivo | Stack | Ejecutar |
| --- | --- | --- |
| `src/deep_clone.py` | Python 3.9+ (solo stdlib) | `python src/deep_clone.py` |
| `src/deep-clone.js` | Node.js 17+ (`structuredClone`) | `node src/deep-clone.js` |
| `src/DeepClone.java` | Java 11+ | `javac -d src src/DeepClone.java && java -cp src DeepClone` |

Cada ejecución muestra el mismo escenario: un objeto con una fecha, un `Set`, una estructura anidada y una referencia circular o hija. El camino JSON falla o pierde tipos; el clonado nativo (`copy.deepcopy`, `structuredClone`, constructor de copia) conserva cada tipo y produce copias completamente independientes.

Java no tiene equivalente a `structuredClone` en el JDK; el deep clone idiomático es un constructor de copia o una librería (`SerializationUtils.clone`, MapStruct). El `copy.deepcopy` de Python es el equivalente built-in más cercano y maneja ciclos por defecto.
