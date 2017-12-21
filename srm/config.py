"""
Manage global and local configuration data.
"""

import os
from typing import Optional

_GLOBAL_PATH = "~/.srmconfig"
_LOCAL_PATH = ".srm/config"


class Conf:
    """Config store."""

    def __init__(self, path: str, parent: Optional['Conf']=None) -> None:
        path = os.path.expanduser(path)
        self.path = os.path.abspath(path)
        self.parent = parent

    def exists(self) -> bool:
        """Return True if config exists."""
        return os.path.exists(self.path) and os.path.isfile(self.path)

    def load(self) -> None:
        """Loads all data from the config file."""
        pass

    def save(self) -> None:
        """Save all values to the config file."""
        if self.parent:
            self.parent.save()

    def create(self) -> None:
        """Create the config file and all necessary directory paths."""
        pass
