"""
Load and query XML data that describes ROM game collections.
"""

import collections
import io
import os
import zipfile
from typing import Set
from xml.etree import ElementTree

import attr
import boltons.cacheutils


class DatafileXml:
    """Parse a DAT XML file (datafile DTD)."""

    def __init__(self, file_path):
        tree = ElementTree.parse(file_path,)
        self._root = tree.getroot()
        self._header = Header.fromXml(self._root.find('header'))

    @property
    def name(self):
        return self._header.name

    @property
    def description(self):
        return self._header.description

    @property
    def version(self):
        return self._header.version

    @property
    def author(self):
        return self._header.author

    @property
    def date(self):
        return self._header.date

    @property
    def homepage(self):
        return self._header.homepage

    @property
    def url(self):
        return self._header.url

    @boltons.cacheutils.cachedproperty
    def roms(self):
        roms = []
        for game in self._root.findall('game'):
            description = game.find('description')
            rom = game.find('rom')
            roms.append(
                ROM(
                    name=game.get('name'),
                    description=description.text,
                    file=rom.get('name'),
                    size=rom.get('size'),
                    crc=rom.get('crc'),
                    md5=rom.get('md5'),
                ))
        return set(roms)

    @boltons.cacheutils.cachedproperty
    def crcs(self):
        return set(r.crc for r in self.roms)

    @boltons.cacheutils.cachedproperty
    def md5s(self):
        return set(r.md5 for r in self.roms)

    def matching(self, crc=None, md5=None):
        if crc:
            return self._crc_index[crc]
        elif md5:
            return self._md5_index[md5]
        else:
            raise ValueError('Method called with no arguments')


class XmlToAttrs:
    """Helper base class to extract XML fields from an element and build an Attrs class."""

    @classmethod
    def fromXml(cls, h: ElementTree.Element):
        args = (h.find(i) for i in cls.__slots__)
        return cls(**{i.tag: i.text for i in args if i is not None})


@attr.s(frozen=True, slots=True, auto_attribs=True)
class Header(XmlToAttrs):
    """ROM Datfile XML header info."""
    name: str  # official name of DAT
    description: str  # extended name
    version: str  # numeric version (e.g. 2.40.900  or 20171210-4500)
    author: str  # contributors or release group
    date: str = ''
    homepage: str = ''
    url: str = ''


@attr.s(frozen=True, slots=True, auto_attribs=True)
class ROM(XmlToAttrs):
    """ROM object defined for one or more Games."""
    name: str  # file name
    size: int  # bytes
    merge: str = ''  # merge name
    crc: str = ''
    md5: str = ''
    sha1: str = ''


@attr.s(frozen=True, slots=True, auto_attribs=True)
class Game(XmlToAttrs):
    """Game record with one or more ROMs."""
    name: str  # file name
    description: str  # common name (can be same as 'name')
    roms: Set[ROM]  # collection of ROMs required by the game

    cloneof: str = ''
    isbios: bool = False
    manufacturer: str = ''
    romof: str = ''
    year: str = ''
