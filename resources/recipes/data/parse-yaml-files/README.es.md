# Analizar Archivos YAML

Ejemplos ejecutables de parseo YAML en Python (PyYAML), JavaScript (js-yaml) y Java (SnakeYAML), todos leyendo el mismo `config.yaml` — incluyendo anchors, merge keys (`<<:`) y listas en flow style.

Recurso complementario de https://stackpractices.com/es/recipes/parse-yaml-files/

## Ejecutar

```bash
python parse_yaml.py            # requiere: pip install pyyaml
node parse-yaml.mjs             # requiere: npm install js-yaml
javac ParseYaml.java && java ParseYaml   # requiere: snakeyaml en el classpath
```

Usa siempre `safe_load`/`safe_dump` (Python) o el `yaml.load` por defecto (js-yaml) para archivos no confiables.
