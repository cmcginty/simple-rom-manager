"""
The "status" command for SRM.
"""

import click


@click.command(name='status')
def cli() -> None:
    """Show ROM state and info."""
    click.echo('temp status')
