"""
The default module run when imported from the command line and also the main entry point defined in
setup.py.  Ex:

    python3 -m srm
"""

import click

from . import __version__, cli


@click.group()
@click.version_option(__version__)
def main() -> None:
    """Simple ROM Manager - A basic command-line ROM set manager."""


main.add_command(cli.init)
main.add_command(cli.status)
main(prog_name='srm')  # pylint: disable=unexpected-keyword-arg
