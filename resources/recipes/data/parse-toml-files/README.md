# Parse and Write TOML Files

Companion resource for [Parse and Write TOML Files](https://stackpractices.com/recipes/parse-toml-files/).

## Files

| File | Description |
|------|-------------|
| `config.toml` | Example TOML configuration with nested tables, arrays of tables, and dates |
| `parse_toml.py` | Python parser and writer using `tomllib` and `tomli-w` |
| `parse_toml.js` | JavaScript parser and writer using `@iarna/toml` |
| `parse_toml.java` | Java parser using `tomlj` |
| `validate_toml.py` | TOML validation with Pydantic |

## Usage

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
