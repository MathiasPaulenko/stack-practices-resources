# Comparar objetos JSON — Archivos complementarios

Diffs ejecutables de la receta de StackPractices:
[Comparar objetos JSON](https://stackpractices.com/es/recipes/diff-json-objects/)

| Archivo | Qué es |
|---------|--------|
| `json_diff.py` | Diff recursivo en Python sin dependencias: imprime rutas añadidas/eliminadas/cambiadas |
| `diff-json.js` | El mismo recorrido en Node, más el modo `--patch` para salida RFC 6902 vía `fast-json-patch` |
| `JsonDiff.java` | Diff recursivo sobre el árbol Jackson (necesita `jackson-databind` en el classpath) |
| `staging.json` / `prod.json` | Payloads de ejemplo: una configuración que se desvió entre entornos |

## Inicio rápido

```bash
# Python, sin dependencias
python json_diff.py staging.json prod.json

# Node, sin dependencias
node diff-json.js staging.json prod.json

# Node, parche RFC 6902
npm install fast-json-patch
node diff-json.js --patch staging.json prod.json

# Java (requiere los jars de jackson en el classpath)
javac -cp "jackson-databind.jar;jackson-core.jar;jackson-annotations.jar" JsonDiff.java
java -cp ".;jackson-databind.jar;jackson-core.jar;jackson-annotations.jar" JsonDiff staging.json prod.json
```

Salida esperada sobre los archivos de ejemplo: tres cambios — `/db/host`
modificado, `/features/1` añadido, `/logLevel` añadido.
