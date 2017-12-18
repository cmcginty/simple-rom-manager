"""
Simple ROM Manager - A basic command-line ROM set manager.
"""

# These values are exported for case when user runs `pydoc srm` or `dir(srm)`.
# It is generally not a good practice for setup.py to import this module directly.

import pbr.version  # type: ignore

__author__ = 'Patick C. McGinty'
__email__ = 'casey.mcginty@gmail.com'
__version__ = pbr.version.VersionInfo('srm').release_string()
