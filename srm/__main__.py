"""
The default module run when imported from the command line and also the main entry point defined in
setup.py.  Ex:

    python3 -m srm
"""

import click

from . import __version__, status


@click.group()
@click.version_option(__version__)
def cli() -> None:
    """Main command-line entry method."""


cli.add_command(status.cli)

if __name__ == '__main__':
    cli()
