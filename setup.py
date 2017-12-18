#!/usr/bin/env python
"""Minmal setuptools entry point configured by Python Build Reasonableness (PBR)."""

from setuptools import setup  # type: ignore

setup(setup_requires=['pbr'], pbr=True)
