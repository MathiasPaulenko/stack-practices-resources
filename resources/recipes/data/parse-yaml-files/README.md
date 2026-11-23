# Parse YAML Files

Runnable YAML parsing examples in Python (PyYAML), JavaScript (js-yaml), and Java (SnakeYAML), all reading the same `config.yaml` — including anchors, merge keys (`<<:`), and flow-style lists.

Companion resource for https://stackpractices.com/recipes/parse-yaml-files/

## Run

```bash
python parse_yaml.py            # requires: pip install pyyaml
node parse-yaml.mjs             # requires: npm install js-yaml
javac ParseYaml.java && java ParseYaml   # requires: snakeyaml on the classpath
```

Always use `safe_load`/`safe_dump` (Python) or the default `yaml.load` (js-yaml) for untrusted files.
