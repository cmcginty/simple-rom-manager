"""
Manage global and local configuration data.
"""

import os
from collections import abc
from typing import Dict  # pylint: disable=unused-import
from typing import Any, Iterator, List, Optional, Set, Tuple

import toml  # type: ignore
from boltons import funcutils, iterutils  # type: ignore

# pylint: disable=notimplemented-raised, raising-bad-type

_LOCAL_PATH = ".srm/config"

_GLOBAL_PATH = "~/.srmconfig"
_GLOBAL_KEYS = {'my.temp.key'}


class Conf(abc.MutableMapping):
    """Config store, backed by a TOML formatted file."""

    def __init__(self, path: str, valid_keys: Optional[Set[str]] = None) -> None:
        """
        :param path: Relative or absolute path of the config file to use.
        :param valid_keys: When defined, __setitem__ will reject key that are not found in this
                           iterable.
        """
        self._path = os.path.expanduser(path)
        self._valid_keys = valid_keys
        self._toml_dict = {}  # type: Dict[str,Any]

    def exists(self) -> bool:
        """Return True if config exists."""
        return os.path.exists(self._path) and os.path.isfile(self._path)

    def load(self, create: bool = False) -> None:
        """
        Load all data from the config file.
        :param create: When True, the path and config will be created instead of raising an
                       exception.
        """
        try:
            with open(self._path) as f:
                self._toml_dict = toml.load(f)
        except FileNotFoundError:
            if create:
                basedir = os.path.dirname(self._path)
                os.makedirs(basedir)
                open(self._path, 'w').close()
            else:
                raise

    def dump(self) -> None:
        """Dump all values to the config file."""
        with open(self._path, "w+") as f:
            toml.dump(self._toml_dict, f)

    def __getitem__(self, k: str) -> Any:
        return iterutils.get_path(self._toml_dict, k)

    def __setitem__(self, k: str, v: Any) -> None:
        if self._valid_keys and k not in self._valid_keys:
            raise KeyError(f"Key {k} is not allowed")

        nested_tables, k = Conf._extract_table_list(k)
        table = self._toml_dict
        for i in nested_tables:
            table = table.setdefault(i, dict())
        table[k] = v

    def __delitem__(self, k: str) -> None:
        nested_tables, k = Conf._extract_table_list(k)
        table = iterutils.get_path(self._toml_dict, nested_tables)
        del table[k]

    def __iter__(self) -> Iterator:
        raise NotImplemented

    def __len__(self) -> int:
        raise NotImplemented

    @staticmethod
    def _extract_table_list(k: str) -> Tuple[List[str], str]:
        tables = k.split('.')
        return tables, tables.pop(-1)


# Callable that will always return the global config.
GlobalConf = funcutils.partial(Conf, _GLOBAL_PATH, _GLOBAL_KEYS)  # pylint: disable=invalid-name


class LocalConf(Conf):
    """
    Load and store keys to a local TOML config file. When a key is not in the local configuration,
    defer to the global TOML file.
    """

    def __init__(self, path: Optional[str] = None) -> None:
        super().__init__(path or _LOCAL_PATH)
        self._global = GlobalConf()

    def load(self, create: bool = False) -> None:
        super().load(create)
        self._global.load(create)

    def dump(self) -> None:
        super().dump()
        self._global.dump()

    def __getitem__(self, k: str) -> Any:
        try:
            return super().__getitem__(k)
        except KeyError:
            return self._global.__getitem__(k)
