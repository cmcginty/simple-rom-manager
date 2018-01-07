"""
File-like objects used to scan and create directories and archives of files.

The goal of this module is to abstract the tedious logic required read and modify files and
directories within archives, as well as nested archives.
"""

import hashlib
import os
import pathlib
import zlib
from typing import Callable

# Path() -> PosixPath or WindowsPath
# where:
#   PosixPath   -> (Path,PurePosixPath)   -> PurePath -> os.PathLike
#   WindowsPath -> (Path,PureWindowsPath) -> PurePath -> os.PathLike
#
# Path() behaves as a factory in that it delegates to Posix or WindowsPath class initializers.
# However, when used directly PurePath() initializer will delegate to PurePosixPath or
# PureWindowsPath.  Which yields:
#   PurePosixPath   -> PurePath
#   PureWindowsPath -> PurePath
#
# Path uses composition to add a system-aware Accessor as a delegate for all file access functions
# like stat, open, chmod, rmdir, mkdir, rename, etc. Since Python os module already handles the
# internals path differences between windows and posix, pathlib only has one default NormalAccessor.
# Extending to non-path object will require at-least a custom Accessor.
#
# The Accessor is directly injected in Path._init, therefore this method must be patched and/or
# modified by a sub-class. It is probably not sufficient to merely create a new Accessor as the
# abstraction seems to expect all path-like object to behave in the same manor.
#
# Path can be internally initialized with a template accessors, providing a way to read/modify
# path-like objects. This feature allows methods to safely return mutated versions of the instance.
# See resolve() and absolute().
#
# The other key delegation class is Selector, and handles various types of traversals when iterating
# over directories and files. The selector instance is created using pathlib._make_selector()
# internal. It will likely be necessary to extend all of the selector classes so that they can
# detect and initialize custom Path objects.
#
# Selector must be sub-classed and implement _select_from() method to perform the actual Path yield.
# It also depends on Path._make_child_relpath() -> PurePath._from_parsed_parts(). These also will
# need to be made aware of custom path-like objects.

# Step 2:
#   * Create a basic ZipPath object that can be returned by Path()
#   * Update Path.glob() so it can detect and return a ZipPath() object by matching the extension.
#   * Investigate context manager support?


class Path(pathlib.Path):
    """Extend the built-in pathlib.Path class to support additional methods."""

    _READ_SIZE = 1024 * 32

    def __new__(cls, *args: os.PathLike, **kwargs: os.PathLike) -> 'Path':
        if cls is Path:
            cls = WindowsPath if os.name == 'nt' else PosixPath
        return super().__new__(cls, *args, **kwargs)

    def crc(self) -> str:
        """Return CRC hash of file."""
        if self.is_dir():
            raise IsADirectoryError
        crc = 0
        with self.open('rb') as f:
            buf = f.read(self._READ_SIZE)
            while buf:
                crc = zlib.crc32(buf, crc)
                buf = f.read(self._READ_SIZE)
        return '{:08x}'.format(crc & 0xFFFF_FFFF)

    def md5(self) -> str:
        """Return MD5 hash of file."""
        return self._hashlib(hashlib.md5)

    def sha1(self) -> str:
        """Return SHA1 hash of file."""
        return self._hashlib(hashlib.sha1)

    def _hashlib(self, hash_fn: Callable) -> str:
        if self.is_dir():
            raise IsADirectoryError
        hasher = hash_fn()
        with self.open('rb') as f:
            buf = f.read(self._READ_SIZE)
            while buf:
                hasher.update(buf)
                buf = f.read(self._READ_SIZE)
        return str(hasher.hexdigest())


class PosixPath(Path, pathlib.PosixPath):
    """Concrete POSIX Path."""
    __slots__ = ()


class WindowsPath(Path, pathlib.WindowsPath):  # pylint: disable=abstract-method
    """Concrete Windows Path."""
    __slots__ = ()
