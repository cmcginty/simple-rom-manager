"""
Load and query XML data that describes ROM game collections.
"""

from typing import Any, Iterable, Set
from xml.etree import ElementTree

import attr  # type: ignore

# import boltons.cacheutils  # type: ignore


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

    @property
    def games(self) -> Iterable['Game']:
        """Iterable of <game> tag elements from DAT."""
        for game in self._root.iter('game'):
            roms = frozenset({ROM.from_xml(r) for r in game.iter('rom')})
            yield Game.from_xml(game, roms=roms)

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
    def from_xml(cls, root: ElementTree.Element, **cls_kwargs: Any) -> Any:
        """
        Dynamically extract attrs fields from XML root element attributes and sub-tags to initialize
        a new cls() instance.

        :param root: XML element to extract class fields from.
        :param cls_kwargs: Additional kwargs passed into the class constructor.
        """
        # Create a combined dict of root attributes and sub-tags.
        cls_kwargs.update(root.attrib)
        cls_kwargs.update({i.tag: i.text or '' for i in root.iter() if i is not root})
        # Init the class using only the expected fields defined by attrs declarations.
        init_kwds = list(i.name for i in iter(attr.fields(cls)))
        return cls(**{k: v for k, v in cls_kwargs.items() if k in init_kwds})  # type: ignore


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
    merge: str = ''  # merge file name, indicates file was merged from "cloneof"
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
