"""
Simple ROM Manager - A basic command-line ROM set manager.
"""

# These values are exported for case when user runs `pydoc srm` or `dir(srm)`.
# It is generally not a good practice for setup.py to import this module directly.

from srm._version import __version__

from srm.__about__ import (
    __author__,
    __copyright__,
    __email__,
    __license__,
    __summary__,
    __title__,
    __uri__,
)
