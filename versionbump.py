"""An auto-increment tool for version strings."""

import unittest.mock
from typing import Any

import click
from click.testing import CliRunner  # type: ignore
from pbr.version import VersionInfo, SemanticVersion  # type: ignore

__version__ = '0.2'


@click.command()
@click.argument('package')
@click.option('--major', 'inc_kwargs', flag_value={'major': True}, help='Increment major number.')
@click.option('--minor', 'inc_kwargs', flag_value={'minor': True}, help='Increment minor number.')
@click.option('--patch', 'inc_kwargs', flag_value={}, default=True, help='Increment patch number.')
def cli(package: str, inc_kwargs: dict) -> None:
    """Bump a MAJOR.MINOR.PATCH version string at the specified index location or 'patch' digit."""

    semver = VersionInfo(package).semantic_version()

    # Pre-decrement a "dev" version to get the real version tuple.
    if 'dev' in semver.version_tuple():
        semver = semver.decrement()

    semver = semver.increment(**inc_kwargs)
    click.echo(semver.release_string(), nl=False)


if __name__ == '__main__':
    cli()  # pylint: disable=no-value-for-parameter


# pylint: disable=missing-docstring,invalid-name
class TestCase(unittest.TestCase):

    def setUp(self):  # type: ignore
        self.runner = CliRunner()

    @unittest.mock.patch.object(VersionInfo, 'semantic_version',
                                return_value=SemanticVersion(0, 0, 0))
    def test_patch_arg(self, _: Any) -> None:
        result = self.runner.invoke(cli, ['dummy', '--patch'])
        self.assertEqual('0.0.1', result.output)

    @unittest.mock.patch.object(VersionInfo, 'semantic_version',
                                return_value=SemanticVersion(0, 0, 0))
    def test_minor_arg(self, _: Any) -> None:
        result = self.runner.invoke(cli, ['dummy', '--minor'])
        self.assertEqual('0.1.0', result.output)

    @unittest.mock.patch.object(VersionInfo, 'semantic_version',
                                return_value=SemanticVersion(0, 0, 0))
    def test_major_arg(self, _: Any) -> None:
        result = self.runner.invoke(cli, ['dummy', '--major'])
        self.assertEqual('1.0.0', result.output)

    @unittest.mock.patch.object(VersionInfo, 'semantic_version',
                                return_value=SemanticVersion(0, 0, 1, None, None, 1))
    def test_patch_arg_on_dev_ver(self, _: Any) -> None:
        result = self.runner.invoke(cli, ['dummy', '--patch'])
        self.assertEqual('0.0.1', result.output)
