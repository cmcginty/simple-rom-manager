#!/usr/bin/env python
"""Minmal setuptools entry point configured by Python Build Reasonableness (PBR)."""

from setuptools import setup  # type: ignore

setup(
    setup_requires=['pbr', 'pytest-runner'],
    pbr=True,
    # extra metadata that PBR ignores
    long_description_content_type='text/markdown; charset=UTF-8',
    python_requires='>=3.6',
    tests_require=['pytest'],
)
