"""Click example: decorator-based CLI with env var support."""

import os

try:
    import click
except ImportError:
    click = None


if click:

    @click.command()
    @click.argument("input")
    @click.option("--output", "-o", default="out.txt", help="Output file")
    @click.option("--verbose", "-v", is_flag=True, help="Verbose mode")
    @click.option("--api-key", envvar="API_KEY", help="API key from env")
    def cli(input, output, verbose, api_key):
        """Process files with Click."""
        click.echo(f"Input: {input}, Output: {output}, Verbose: {verbose}")
        if api_key:
            click.echo(f"API key loaded from env ({len(api_key)} chars)")

    if __name__ == "__main__":
        cli()
