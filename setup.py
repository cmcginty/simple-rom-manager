"""A setuptools based setup module.

See:
    https://packaging.python.org/en/latest/distributing.html
    https://github.com/pypa/sampleproject
"""

import os.path
import subprocess

from setuptools import setup, find_packages  # type: ignore

import srm

CWD = os.path.abspath(os.path.dirname(__file__))


def version() -> str:
    """Export version from git and store to the package dir."""
    ver = 'unknown'
    try:
        raw = subprocess.check_output(["git", "describe", "--tags"])
        ver = raw.decode('utf-8').strip()
        ver = ver.rsplit('-', 1)[0]  # remove git hash
    except subprocess.CalledProcessError:
        pass
    with open('srm/_version.py', 'w') as f:
        print('"""Auto-generated version file from setup.py"""', file=f)
        print(f'__version__ = "{ver}"', file=f)
    return ver


def long_description() -> str:
    """Get the long description from the README file."""
    with open(os.path.join(CWD, 'README.md'), encoding='utf-8') as f:
        return f.read()

AUTHOR = srm.__author__
EMAIL = srm.__email__
NAME = srm.__long_name__
URL = srm.__url__
VERSION = version()

setup(
    name=NAME,
    author=AUTHOR,
    author_email=EMAIL,
    description=srm.__doc__.strip(),
    long_description=long_description(),
    url=URL,
    download_url=f"https://github.com/cmcginty/{NAME}/raw/master/dist/{NAME}-{VERSION}.tar.gz",
    version=version(),

    license='MIT',

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
