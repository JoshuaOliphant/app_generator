"""Command line interface for generating AI-powered applications."""

import click
from pathlib import Path
import yaml
from .generator import AppGenerator

@click.command()
@click.argument('output_dir', type=click.Path())
@click.option(
    '--openapi', '-o',
    type=click.Path(exists=True, dir_okay=False),
    required=True,
    help='Path to OpenAPI specification file'
)
@click.option(
    '--integrations', '-i',
    type=click.Path(exists=True, dir_okay=False),
    required=True,
    help='Path to integrations configuration file'
)
@click.option(
    '--name',
    type=str,
    required=True,
    help='Name of the generated application'
)
def generate(output_dir: str, openapi: str, integrations: str, name: str):
    """Generate an AI-powered application with SQLite database."""
    output_path = Path(output_dir)
    openapi_path = Path(openapi)
    integrations_path = Path(integrations)

    try:
        # Only read the integrations file
        with integrations_path.open() as f:
            integrations_spec = yaml.safe_load(f)

        # Basic validation
        if 'database' not in integrations_spec or integrations_spec['database']['type'] != 'sqlite':
            raise ValueError("Only SQLite database is supported in this version")

        # Create generator with the file path instead of parsed content
        generator = AppGenerator(
            name=name,
            openapi_path=openapi_path,  # Pass the path instead of parsed content
            integrations_spec=integrations_spec,
            output_dir=output_path
        )
        generator.generate()

        click.echo(f"\nSuccessfully generated application in {output_path}")

        # Print next steps
        click.echo("\nNext steps:")
        click.echo(f"1. cd {output_path}")
        click.echo(f"2. python -m venv .venv")
        click.echo(f"3. source .venv/bin/activate")
        click.echo(f"4. pip install -r requirements.txt")
        click.echo(f"5. uvicorn {name}.app:app --reload")

    except Exception as e:
        click.echo(f"Error generating application: {e}", err=True)
        raise click.Abort()
