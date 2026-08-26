# Analizar y Escribir Archivos TOML

Recurso companion para [Analizar TOML](https://stackpractices.com/es/recipes/parse-toml-files/).

## Archivos

| Archivo | Descripción |
|---------|-------------|
| `config.toml` | Configuración TOML de ejemplo con tablas anidadas, arrays de tablas y fechas |
| `parse_toml.py` | Parser y escritor en Python usando `tomllib` y `tomli-w` |
| `parse_toml.js` | Parser y escritor en JavaScript usando `@iarna/toml` |
| `parse_toml.java` | Parser en Java usando `tomlj` |
| `validate_toml.py` | Validación TOML con Pydantic |

## Uso

### Python

```bash
python parse_toml.py
python validate_toml.py
```

### JavaScript

```bash
npm install @iarna/toml
node parse_toml.js
```

### Java

```bash
# Maven: org.tomlj:tomlj:1.1.0
javac parse_toml.java && java parse_toml
```
