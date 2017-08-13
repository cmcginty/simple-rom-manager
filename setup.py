"""A setuptools based setup module.

See:
https://packaging.python.org/en/latest/distributing.html
https://github.com/pypa/sampleproject
"""

from setuptools import setup, find_packages  # type: ignore

import srm


def long_description() -> str:
    """Get the long description from the README file."""
    try:
        import pypandoc  # type: ignore
        return str(pypandoc.convert('README.md', 'rst'))
    except Exception:  # pylint: disable=broad-except
        return open('README.md').read()

NAME = srm.__long_name__
VERSION = srm.__version__
AUTHOR = srm.__author__
EMAIL = srm.__email__
DESCRIPTION = srm.__doc__.strip()
URL = srm.__url__

setup(
    name=NAME,
    author=AUTHOR,
    author_email=EMAIL,
    description=DESCRIPTION,
    long_description=long_description(),
    url=URL,
    download_url=f"https://github.com/cmcginty/{NAME}/raw/master/dist/{NAME}-{VERSION}.tar.gz",
    version=VERSION,

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
