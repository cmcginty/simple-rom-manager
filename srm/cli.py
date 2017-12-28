"""
Entry points for all of the primary SRM commands.
"""
import click

from . import config


@click.command()
def init() -> None:
    """Initialize the current directory for SRM."""
    conf = config.LocalConf()
    if not conf.exists():
        conf.load(create=True)
    else:
        click.secho("Directory is already initialized!", fg='red')


@click.command()
def status() -> None:
    """Show ROM state and info."""
    conf = config.LocalConf()
    if not conf.exists():
        raise click.ClickException("Directory is not initialized! Try the 'init' command.")
    click.echo("temp status")
