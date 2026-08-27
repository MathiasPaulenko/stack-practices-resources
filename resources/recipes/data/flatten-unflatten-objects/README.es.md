# Aplanar y Reconstruir Objetos Anidados — Ejemplos Companion

Ejemplos ejecutables para aplanar y reconstruir objetos anidados en Python, JavaScript y Java.

## Archivos

| Archivo | Lenguaje | Qué hace |
| --- | --- | --- |
| `flatten.py` | Python | Aplanar/reconstruir con división de claves por regex |
| `flatten.js` | JavaScript (Node.js) | Aplanar/reconstruir con división de claves por RegExp |
| `FlattenUtil.java` | Java | Aplanar/reconstruir con LinkedHashMap y List |
| `sample.json` | JSON | Objeto anidado de ejemplo para pruebas |

## Ejecución

### Python

```bash
python flatten.py
```

### JavaScript

```bash
node flatten.js
```

### Java

```bash
javac FlattenUtil.java
java FlattenUtil
```

## Salida esperada

Cada script imprime los pares clave-valor aplanados, el objeto reconstruido, y verifica que el ciclo `flatten(unflatten(flat)) == flat` se cumple.

## Fuente

- [Aplanar y Reconstruir Objetos Anidados](https://stackpractices.com/es/recipes/flatten-unflatten-objects/)
