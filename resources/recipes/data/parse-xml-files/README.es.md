# Analizar Archivos XML — Código de Ejemplo

Ejemplos ejecutables de la receta de StackPractices
[Analizar Archivos XML en Python, Java y JavaScript](https://stackpractices.com/es/recipes/parse-xml-files/).

## Contenido

| Archivo | Qué muestra |
| --- | --- |
| `data.xml` | Catálogo de muestra usado por todos los ejemplos |
| `parse_xml.py` | ElementTree de Python (DOM), XPath, streaming con `iterparse`, `defusedxml` para entrada no confiable |
| `parse-xml.mjs` | Mapeo a objetos con `fast-xml-parser` en Node.js, con `processEntities: false` |
| `ParseXml.java` | JAXP DOM + SAX en Java con configuración de factory segura frente a XXE |

## Ejecutar

```bash
python parse_xml.py          # Python 3.8+, solo librería estándar
node parse-xml.mjs           # npm install fast-xml-parser
javac ParseXml.java && java ParseXml
```

Para `parse_untrusted()` en `parse_xml.py`, instala antes `defusedxml`
(`pip install defusedxml`) y descomenta la llamada en `__main__`.
