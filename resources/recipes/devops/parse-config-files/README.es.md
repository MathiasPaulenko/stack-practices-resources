# Parsear y Validar Archivos de Config — Companion

Ejemplos ejecutables para la receta de StackPractices
[Parsear y Validar Configuración YAML/JSON](https://stackpractices.com/es/recipes/parse-config-files/).

## Archivos

| Archivo | Lenguaje | Descripción |
|---------|----------|-------------|
| `config.yaml` | YAML | Config de ejemplo con sustitución de env vars |
| `config.json` | JSON | Config de ejemplo en formato JSON |
| `load_config.py` | Python | Validación con Pydantic y sustitución de env vars |
| `load_config.js` | JavaScript | Validación de schema con Zod |
| `ConfigLoader.java` | Java | Jackson + Jakarta Validation |
| `load_config.go` | Go | Struct tags + validación manual |

## Inicio rápido

### Python

```bash
pip install pydantic pyyaml
python load_config.py
```

### JavaScript

```bash
npm install yaml zod
node load_config.js
```

### Java

```bash
javac -cp "jackson-databind:jackson-yaml:jakarta-validation-api" ConfigLoader.java
java -cp ".:jackson-databind:jackson-yaml:jakarta-validation-api" ConfigLoader
```

### Go

```bash
go mod init config-loader
go get gopkg.in/yaml.v3
go run load_config.go
```

## Fuente

- [Receta (EN)](https://stackpractices.com/recipes/parse-config-files/)
- [Receta (ES)](https://stackpractices.com/es/recipes/parse-config-files/)
