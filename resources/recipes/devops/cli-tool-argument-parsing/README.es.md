# Parseo de argumentos CLI — Recursos Companion

Ejemplos ejecutables para la [receta de parseo de argumentos CLI](https://stackpractices.com/es/recipes/cli-tool-argument-parsing/) en StackPractices.

## Archivos

| Archivo | Lenguaje | Librería |
|---------|----------|----------|
| `deploy_argparse.py` | Python | argparse (stdlib) |
| `deploy_typer.py` | Python | Typer |
| `deploy_commander.js` | JavaScript | commander.js |
| `DeployCli.java` | Java | picocli |
| `main.go` | Go | cobra |
| `main.rs` | Rust | clap |
| `Cargo.toml` | Rust | dependencias |
| `package.json` | JavaScript | dependencias |
| `docker-compose.yml` | Todos | Docker Compose |

## Inicio rápido

### Python (argparse)

```bash
python deploy_argparse.py prod --version 2.1.0 --dry-run
```

### Python (Typer)

```bash
pip install typer
python deploy_typer.py prod --version 2.1.0 --dry-run
```

### JavaScript (commander.js)

```bash
npm install
node deploy_commander.js deploy prod --version 2.1.0 --dry-run
```

### Java (picocli)

```bash
javac -cp picocli-4.7.0.jar DeployCli.java
java -cp .:picocli-4.7.0.jar DeployCli prod --version 2.1.0 --dry-run
```

### Go (cobra)

```bash
go mod init deploy-cli && go get github.com/spf13/cobra
go run main.go deploy prod --version 2.1.0 --dry-run
```

### Rust (clap)

```bash
cargo run -- deploy prod --version 2.1.0 --dry-run
```

## Testing

Cada ejemplo acepta los mismos argumentos y produce el mismo output:

```
Deploying 2.1.0 to prod
(dry run mode)
```

Corré con `--help` para ver el texto de ayuda auto-generado:

```bash
python deploy_argparse.py --help
node deploy_commander.js --help
java DeployCli --help
go run main.go --help
cargo run -- --help
```
