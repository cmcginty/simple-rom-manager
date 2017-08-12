"""An auto-increment tool for version strings."""

import sys
import unittest

import click
from click.testing import CliRunner  # type: ignore

__version__ = '0.1'

MIN_DIGITS = 2
MAX_DIGITS = 3


@click.command()
@click.argument('version')
@click.option('--major', 'bump_idx', flag_value=0, help='Increment major number.')
@click.option('--minor', 'bump_idx', flag_value=1, help='Increment minor number.')
@click.option('--patch', 'bump_idx', flag_value=2, default=True, help='Increment patch number.')
def cli(version: str, bump_idx: int) -> None:
    """Bumps a MAJOR.MINOR.PATCH version string at the specified index location or 'patch' digit. An
    optional 'v' prefix is allowed and will be included in the output if found."""
    prefix = version[0] if version[0].isalpha() else ''
    digits = version.lower().lstrip('v').split('.')

    if len(digits) > MAX_DIGITS:
        click.secho('ERROR: Too many digits', fg='red', err=True)
        sys.exit(1)

    digits = (digits + ['0'] * MAX_DIGITS)[:MAX_DIGITS]  # Extend total digits to max.
    digits[bump_idx] = str(int(digits[bump_idx]) + 1)  # Increment the desired digit.

    # Zero rightmost digits after bump position.
    for i in range(bump_idx + 1, MAX_DIGITS):
        digits[i] = '0'
    digits = digits[:max(MIN_DIGITS, bump_idx + 1)]  # Trim rightmost digits.
    click.echo(prefix + '.'.join(digits), nl=False)


if __name__ == '__main__':
    cli()  # pylint: disable=no-value-for-parameter


# pylint: disable=missing-docstring,invalid-name
class TestCase(unittest.TestCase):

    def setUp(self):  # type: ignore
        self.runner = CliRunner()

    def test_greater_than_max_digits_is_error(self):  # type: ignore
        result = self.runner.invoke(cli, ['0.0.0.0'])
        self.assertIn('ERROR', result.output)
        self.assertEqual(result.exit_code, 1)

    def test_v_prefix_is_kept_in_result(self):  # type: ignore
        result = self.runner.invoke(cli, ['v0.0.0'])
        self.assertEqual('v0.0.1', result.output)

    def test_patch_arg(self):  # type: ignore
        result = self.runner.invoke(cli, ['0.0.0', '--patch'])
        self.assertEqual('0.0.1', result.output)

    def test_minor_arg(self):  # type: ignore
        result = self.runner.invoke(cli, ['0.0.0', '--minor'])
        self.assertEqual('0.1', result.output)

    def test_major_arg(self):  # type: ignore
        result = self.runner.invoke(cli, ['0.0.0', '--major'])
        self.assertEqual('1.0', result.output)

    def test_short_ver_with_patch_arg(self):  # type: ignore
        result = self.runner.invoke(cli, ['1', '--patch'])
        self.assertEqual('1.0.1', result.output)

    def test_short_ver_with_minor_arg(self):  # type: ignore
        result = self.runner.invoke(cli, ['1', '--minor'])
        self.assertEqual('1.1', result.output)

    def test_short_ver_with_major_arg(self):  # type: ignore
        result = self.runner.invoke(cli, ['1', '--major'])
        self.assertEqual('2.0', result.output)
