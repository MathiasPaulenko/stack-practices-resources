# Analizar Argumentos CLI — Recursos Companion

Código companion de la receta [Analizar Argumentos CLI](https://stackpractices.com/es/recipes/parse-command-line-arguments/) en StackPractices.

## Contenidos

|Archivo|Descripción|
|---------|-------------|
|`argparse_example.py`|Python argparse con flags, opciones tipadas y subcomandos|
|`click_example.py`|Python Click con decoradores y soporte de variables de entorno|
|`commander_example.js`|Node.js Commander con API fluent y subcomandos|
|`picocli_example.java`|Java picocli con anotaciones y subcomandos|
|`test_cli_examples.py`|Tests unitarios para los ejemplos de argparse y Click|
|`README.md`|README en inglés|
|`README.es.md`|README en español|

## Cómo ejecutar los ejemplos

### Instalar dependencias

```bash
pip install click pytest
npm install commander
```

### Ejecutar ejemplo Python argparse

```bash
python argparse_example.py input.txt -o output.txt -v
python argparse_example.py input.txt push --force
```

### Ejecutar ejemplo Python Click

```bash
python click_example.py input.txt -o output.txt -v
API_KEY=secret123 python click_example.py input.txt
```

### Ejecutar ejemplo Node.js Commander

```bash
node commander_example.js input.txt -o output.txt -v
node commander_example.js push --force
```

### Ejecutar ejemplo Java picocli

```bash
# Compilar con picocli en el classpath
javac -cp picocli-4.7.6.jar picocli_example.java
java -cp .:picocli-4.7.6.jar picocli_example input.txt -o output.txt -v
```

### Ejecutar tests unitarios

```bash
pytest test_cli_examples.py -v
```
