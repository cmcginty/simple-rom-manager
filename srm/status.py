"""
The "status" command for SRM.
"""

import click


@click.command(name='status')
def cli():
    """Show ROM state and info."""
    click.echo('temp status')
