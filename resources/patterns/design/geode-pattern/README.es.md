# Patrón Geode

Recursos de apoyo del [Patrón Geode](https://stackpractices.com/es/patterns/geode-pattern/) en StackPractices.

Tres implementaciones ejecutables de un clúster particionado: cada nodo posee un rango de hash, guarda sus propios datos y falla de forma aislada. Las demos insertan usuarios, imprimen estadísticas por shard y luego matan un nodo para mostrar que solo su shard se ve afectado.

## Archivos

| Archivo | Descripción |
|---------|-------------|
| `geode_cluster.py` | Python (dataclasses + hashlib); ejecutar con `python geode_cluster.py` |
| `geode_cluster.js` | Node.js (crypto + Map); ejecutar con `node geode_cluster.js` |
| `GeodeCluster.java` | Java 16+ (MessageDigest + HashMap); ejecutar con `javac GeodeCluster.java && java GeodeCluster` |

## Qué probar

- Añade un método `restore_node`/`restoreNode` y recupera `node-2` a mitad de la ejecución.
- Cambia `num_nodes` y observa cómo los rangos fijos redistribuyen todas las claves — luego busca consistent hashing para ver por qué los sistemas en producción evitan los rangos fijos.
- Registra en qué nodo cae cada usuario y comprueba que la distribución es más o menos uniforme.

## Notas

- `owns_key`/`ownsKey` es la única fuente de verdad del enrutado — `find_node`/`findNode` le delega para que la comprobación de propiedad nunca diverja.
- No hay replicación ni rebalanceo a propósito; la página del patrón cubre consistent hashing y nodos virtuales para eso.
