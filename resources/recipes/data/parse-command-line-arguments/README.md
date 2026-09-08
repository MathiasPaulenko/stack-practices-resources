# Parse Command Line Arguments — Companion Resources

Companion code for the [Parse Command Line Arguments recipe](https://stackpractices.com/recipes/parse-command-line-arguments/) on StackPractices.

## Contents

|File|Description|
|------|-------------|
|`argparse_example.py`|Python argparse with flags, typed options, and subcommands|
|`click_example.py`|Python Click with decorators and env var support|
|`commander_example.js`|Node.js Commander with fluent API and subcommands|
|`picocli_example.java`|Java picocli with annotations and subcommands|
|`test_cli_examples.py`|Unit tests for argparse and Click examples|
|`README.md`|English README|
|`README.es.md`|Spanish README|

## Running the Examples

### Install dependencies

```bash
pip install click pytest
npm install commander
```

### Run Python argparse example

```bash
python argparse_example.py input.txt -o output.txt -v
python argparse_example.py input.txt push --force
```

### Run Python Click example

```bash
python click_example.py input.txt -o output.txt -v
API_KEY=secret123 python click_example.py input.txt
```

### Run Node.js Commander example

```bash
node commander_example.js input.txt -o output.txt -v
node commander_example.js push --force
```

### Run Java picocli example

```bash
# Compile with picocli on classpath
javac -cp picocli-4.7.6.jar picocli_example.java
java -cp .:picocli-4.7.6.jar picocli_example input.txt -o output.txt -v
```

### Run unit tests

```bash
pytest test_cli_examples.py -v
```
