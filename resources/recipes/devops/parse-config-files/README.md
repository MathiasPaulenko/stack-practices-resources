# Parse & Validate Config Files — Companion

Runnable examples for the StackPractices recipe
[Parse and Validate YAML/JSON Configuration](https://stackpractices.com/recipes/parse-config-files/).

## Files

| File | Language | Description |
|------|----------|-------------|
| `config.yaml` | YAML | Sample config with env var substitution |
| `config.json` | JSON | Sample config in JSON format |
| `load_config.py` | Python | Pydantic validation with env var substitution |
| `load_config.js` | JavaScript | Zod schema validation |
| `ConfigLoader.java` | Java | Jackson + Jakarta Validation |
| `load_config.go` | Go | Struct tags + manual validation |

## Quick start

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

## Source

- [Recipe (EN)](https://stackpractices.com/recipes/parse-config-files/)
- [Recipe (ES)](https://stackpractices.com/es/recipes/parse-config-files/)
