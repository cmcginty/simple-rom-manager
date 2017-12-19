#!/usr/bin/env python
"""Minmal setuptools entry point configured by Python Build Reasonableness (PBR)."""

from setuptools import setup  # type: ignore

setup(
    setup_requires=['pbr>=3.1.1', 'setuptools>=38.2.4'],
    pbr=True,
    # extra metadata that PBR ignores
    python_requires='>=3.6',
    long_description_content_type='text/markdown; charset=UTF-8',
)
