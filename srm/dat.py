"""
Load and query XML data that describes ROM game collections.
"""

from typing import Set, Any
from xml.etree import ElementTree

import attr  # type: ignore

# import boltons.cacheutils  # type: ignore

# pylint: disable=missing-docstring


class DatafileXml:
    """Parse a DAT XML file (datafile DTD)."""

    def __init__(self, file_path: str) -> None:
        tree = ElementTree.parse(file_path,)
        self._root = tree.getroot()
        header = self._root.find('header')
        if header is None:
            raise ElementTree.ParseError('DAT file does not contain a valid "header"')
        self._header = Header.from_xml(header)

    @property
    def name(self) -> str:
        """DAT <header><name> field."""
        return str(self._header.name)

    @property
    def description(self) -> str:
        """DAT <header><description> field."""
        return str(self._header.description)

    @property
    def version(self) -> str:
        """DAT <header><version> field."""
        return str(self._header.version)

    @property
    def author(self) -> str:
        """DAT <header><author> field."""
        return str(self._header.author)

    @property
    def date(self) -> str:
        """DAT <header><date> field."""
        return str(self._header.date)

    @property
    def homepage(self) -> str:
        """DAT <header><homepage> field."""
        return str(self._header.homepage)

    @property
    def url(self) -> str:
        """DAT <header><url> field."""
        return str(self._header.url)

    # @boltons.cacheutils.cachedproperty
    # def roms(self) -> Set[ROM]:
    #     roms = []
    #     for game in self._root.findall('game'):
    #         description = game.find('description')
    #         rom = game.find('rom')
    #         roms.append(
    #             ROM(
    #                 name=game.get('name'),
    #                 description=description.text,
    #                 file=rom.get('name'),
    #                 size=rom.get('size'),
    #                 crc=rom.get('crc'),
    #                 md5=rom.get('md5'),
    #             ))
    #     return set(roms)
    #
    # @boltons.cacheutils.cachedproperty
    # def crcs(self) -> Set[str]:
    #     return set(r.crc for r in self.roms)
    #
    # @boltons.cacheutils.cachedproperty
    # def md5s(self) -> Set[str]:
    #     return set(r.md5 for r in self.roms)

    # def matching(self, crc=None, md5=None):
    #     if crc:
    #         return self._crc_index[crc]
    #     elif md5:
    #         return self._md5_index[md5]
    #     else:
    #         raise ValueError('Method called with no arguments')


class XmlToAttrs:  # pylint: disable=too-few-public-methods
    """Helper to generically map XML fields from an element and create an attrs class."""

    @classmethod
    def from_xml(cls, header: ElementTree.Element) -> Any:
        """Dynamically extract attrs fields from XML <header> and create new cls() instance."""
        fields = (i.name for i in iter(attr.fields(cls)))
        xml_el = (header.find(i) for i in fields)  # pylint: disable=no-member
        return cls(**{i.tag: i.text for i in xml_el if i is not None})  # type: ignore


@attr.s(frozen=True, slots=True, auto_attribs=True)  # pylint: disable=too-few-public-methods
class Header(XmlToAttrs):
    """ROM Datfile XML header info."""
    name: str  # official name of DAT
    description: str  # extended name
    version: str  # numeric version (e.g. 2.40.900  or 20171210-4500)
    author: str  # contributors or release group
    date: str = ''
    homepage: str = ''
    url: str = ''


@attr.s(frozen=True, slots=True, auto_attribs=True)  # pylint: disable=too-few-public-methods
class ROM(XmlToAttrs):
    """ROM object defined for one or more Games."""
    name: str  # file name
    size: int  # bytes
    merge: str = ''  # merge name
    crc: str = ''
    md5: str = ''
    sha1: str = ''


@attr.s(frozen=True, slots=True, auto_attribs=True)  # pylint: disable=too-few-public-methods
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
