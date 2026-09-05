import typer

app = typer.Typer()


@app.command()
def deploy(
    environment: str,
    version: str = "latest",
    dry_run: bool = False,
    verbose: bool = False,
):
    typer.echo(f"Deploying {version} to {environment}")
    if dry_run:
        typer.echo("(dry run mode)")


if __name__ == "__main__":
    app()
