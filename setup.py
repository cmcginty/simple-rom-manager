"""A setuptools based setup module.

See:
https://packaging.python.org/en/latest/distributing.html
https://github.com/pypa/sampleproject
"""

import os.path
from setuptools import setup, find_packages

CWD = os.path.abspath(os.path.dirname(__file__))

# Get the long description from the README file
with open(os.path.join(CWD, 'README.md'), encoding='utf-8') as f:
    LONG_DESCRIPTION = f.read()

setup(
    name='simple-rom-manger',
    version='0.1.dev1',

    # Package info
    author='Patrick C. McGinty',
    author_email='casey.mcginty@gmail.com',
    description='A basic command-line ROM set manager.',
    long_description=LONG_DESCRIPTION,
    license='MIT',
    url='http://github.com/cmcginty/simple-rom-manager/',

    # Build details
    packages=find_packages(),
    include_package_data=False,
    python_requires='~=3.6',
    install_requires=[
        'boltons',
        'attrs',
    ],

    # PyPi info
    classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.6',
    ],

    entry_points={
        'console_scripts': [
            'srm = srm.__main__:main',
        ],
    },
)
