# CLI Argument Parsing — Companion Resources

Runnable examples for the [CLI Argument Parsing recipe](https://stackpractices.com/recipes/cli-tool-argument-parsing/) on StackPractices.

## Files

| File | Language | Library |
|------|----------|---------|
| `deploy_argparse.py` | Python | argparse (stdlib) |
| `deploy_typer.py` | Python | Typer |
| `deploy_commander.js` | JavaScript | commander.js |
| `DeployCli.java` | Java | picocli |
| `main.go` | Go | cobra |
| `main.rs` | Rust | clap |
| `Cargo.toml` | Rust | dependencies |
| `package.json` | JavaScript | dependencies |
| `docker-compose.yml` | All | Docker Compose |

## Quick start

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

Each example accepts the same arguments and produces the same output:

```
Deploying 2.1.0 to prod
(dry run mode)
```

Run with `--help` to see auto-generated help text:

```bash
python deploy_argparse.py --help
node deploy_commander.js --help
java DeployCli --help
go run main.go --help
cargo run -- --help
```
