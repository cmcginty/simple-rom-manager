"""A setuptools based setup module.

See:
https://packaging.python.org/en/latest/distributing.html
https://github.com/pypa/sampleproject
"""
# pylint: disable=exec-used, invalid-name

from setuptools import setup, find_packages  # type: ignore


def long_description() -> str:
    """Get the long description from the README file."""
    try:
        import pypandoc  # type: ignore
        return str(pypandoc.convert('README.md', 'rst'))
    except Exception:  # pylint: disable=broad-except
        return open('README.md').read()

exec_vars = {}  # type: ignore

with open("srm/_version.py") as fp:
    exec(fp.read(), exec_vars)

with open("srm/__about__.py") as fp:
    exec(fp.read(), exec_vars)

AUTHOR = exec_vars['__author__']
DESCRIPTION = exec_vars['__summary__']
EMAIL = exec_vars['__email__']
LICENSE = exec_vars['__license__']
NAME = exec_vars['__pypi_name__']
URI = exec_vars['__uri__']
VERSION = exec_vars['__version__']

setup(
    name=NAME,
    author=AUTHOR,
    author_email=EMAIL,
    description=DESCRIPTION,
    long_description=long_description(),
    url=URI,
    download_url=f"https://github.com/cmcginty/{NAME}/raw/master/dist/{NAME}-{VERSION}.tar.gz",
    version=VERSION,

    license=LICENSE,

    entry_points={'console_scripts': ['srm = srm.__main__:cli']},
    packages=find_packages(),
    include_package_data=False,
    python_requires='~=3.6',
    install_requires=[
        'attrs',
        'boltons',
        'click',
    ],

    keywords='rom roms nointro datomatic retro gaming console snes nes games mame retropie',
    # classifier list @ https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: End Users/Desktop',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Operating System :: MacOS :: MacOS X',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: Implementation :: CPython',
        'Topic :: Games/Entertainment',
        'Topic :: System :: Archiving :: Compression',
        'Topic :: System :: Archiving',
        'Topic :: Utilities',
    ],
)
