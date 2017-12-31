"""
Test cases for DAT XML import and processing.
"""

from unittest.mock import mock_open, patch, sentinel, ANY

import pytest

from srm.dat import DatafileXml

PATH = sentinel.PATH

DAT_01 = dict(
    xml="""\
<?xml version="1.0"?>
<!DOCTYPE datafile PUBLIC "-//FB Alpha//DTD ROM Management Datafile//EN" "http://www.logiqx.com/Dats/datafile.dtd">
<datafile>
    <header>
        <name>FB Alpha - SuprGrafx Games</name>
        <description>FB Alpha v0.2.97.42 SuprGrafx Games</description>
        <category>Standard DatFile</category>
        <version>0.2.97.42</version>
        <author>FB Alpha</author>
        <homepage>https://www.fbalpha.com/</homepage>
        <url>https://www.fbalpha.com/</url>
        <clrmamepro forcenodump="ignore"/>
    </header>
    <game name="1941">
        <description>1941 - Counter Attack</description>
        <year>1991</year>
        <manufacturer>Hudson</manufacturer>
        <rom name="1941 - counter attack (japan).pce" size="1048576" crc="8c4588e2"/>
    </game>
    <game name="aldynes">
        <description>Aldynes</description>
        <year>1991</year>
        <manufacturer>Hudson</manufacturer>
        <rom name="aldynes (japan).pce" size="1048576" crc="4c2126b0"/>
    </game>
</datafile>
""",
    header=dict(
        name='FB Alpha - SuprGrafx Games',
        description='FB Alpha v0.2.97.42 SuprGrafx Games',
        version='0.2.97.42',
        author='FB Alpha',
        homepage='https://www.fbalpha.com/',
        url='https://www.fbalpha.com/',
    ),
)

DAT_02 = dict(
    xml="""\
<?xml version="1.0"?>
<!DOCTYPE datafile PUBLIC "-//FB Alpha//DTD ROM Management Datafile//EN" "http://www.logiqx.com/Dats/datafile.dtd">
<datafile>
    <header>
        <name>FB Alpha - Arcade Games</name>
        <description>FB Alpha v0.2.97.42 Arcade Games</description>
        <category>Standard DatFile</category>
        <version>0.2.97.42</version>
        <author>FB Alpha</author>
        <homepage>https://www.fbalpha.com/</homepage>
        <url>https://www.fbalpha.com/</url>
        <clrmamepro forcenodump="ignore"/>
    </header>
    <game name="gtmrb" cloneof="gtmr" romof="gtmr">
        <description>1000 Miglia: Great 1000 Miles Rally (94/05/26)</description>
        <year>1994</year>
        <manufacturer>Kaneko</manufacturer>
        <rom name="mmp0x1.u514" size="524288" crc="6c163f12"/>
        <rom name="mmp1x1.u513" size="524288" crc="424dc7e1"/>
        <rom name="mmd0x1.u124" size="131072" crc="3d7cb329"/>
        <rom name="mm-200-402-s0.bin" merge="mm-200-402-s0.bin" size="2097152" crc="c0ab3efc"/>
        <rom name="mm-201-403-s1.bin" merge="mm-201-403-s1.bin" size="2097152" crc="cf6b23dc"/>
        <rom name="mm-202-404-s2.bin" merge="mm-202-404-s2.bin" size="2097152" crc="8f27f5d3"/>
        <rom name="mm-203-405-s3.bin" merge="mm-203-405-s3.bin" size="524288" crc="e9747c8c"/>
        <rom name="mms1x1.u30" size="131072" crc="9463825c"/>
        <rom name="mms0x1.u29" size="131072" crc="bd22b7d2"/>
        <rom name="mm-300-406-a0.bin" merge="mm-300-406-a0.bin" size="2097152" crc="b15f6b7f"/>
        <rom name="mm-100-401-e0.bin" merge="mm-100-401-e0.bin" size="1048576" crc="b9cbfbee"/>
    </game>
    <game name="gtmr">
        <description>1000 Miglia: Great 1000 Miles Rally (94/07/18)</description>
        <year>1994</year>
        <manufacturer>Kaneko</manufacturer>
        <rom name="u2.bin" size="524288" crc="031799f7"/>
        <rom name="u1.bin" size="524288" crc="6238790a"/>
        <rom name="mmd0x2.u124.bin" size="131072" crc="3d7cb329"/>
        <rom name="mm-200-402-s0.bin" size="2097152" crc="c0ab3efc"/>
        <rom name="mm-201-403-s1.bin" size="2097152" crc="cf6b23dc"/>
        <rom name="mm-202-404-s2.bin" size="2097152" crc="8f27f5d3"/>
        <rom name="mm-203-405-s3.bin" size="524288" crc="e9747c8c"/>
        <rom name="mms1x2.u30.bin" size="131072" crc="b42b426f"/>
        <rom name="mms0x2.u29.bin" size="131072" crc="bd22b7d2"/>
        <rom name="mm-300-406-a0.bin" size="2097152" crc="b15f6b7f"/>
        <rom name="mm-100-401-e0.bin" size="1048576" crc="b9cbfbee"/>
    </game>
</datafile>
""",
    header=dict(
        name='FB Alpha - Arcade Games',
        description='FB Alpha v0.2.97.42 Arcade Games',
        version='0.2.97.42',
        author='FB Alpha',
        homepage='https://www.fbalpha.com/',
        url='https://www.fbalpha.com/',
    ),
)

DAT_03 = dict(
    xml="""\
<?xml version="1.0"?>
<!DOCTYPE datafile PUBLIC "-//Logiqx//DTD ROM Management Datafile//EN" "http://www.logiqx.com/Dats/datafile.dtd">
<datafile>
    <header>
        <name>Nintendo - Game Boy</name>
        <description>Nintendo - Game Boy</description>
        <version>20171226-085946</version>
        <author>C. V. Reynolds, Densetsu, xuom2</author>
        <homepage>No-Intro</homepage>
        <url>http://www.no-intro.org</url>
    </header>
    <game name="Battletoads (Japan)">
        <description>Battletoads (Japan)</description>
        <rom name="Battletoads (Japan).gb" size="131072" crc="331CF7DE" md5="3D57E0391C8191C105A4F015A0C103E9" sha1="666ED5D34F508C8805A67F4400FC01A1F2817E03"/>
    </game>
    <game name="Battletoads (USA, Europe)">
        <description>Battletoads (USA, Europe)</description>
        <rom name="Battletoads (USA, Europe).gb" size="131072" crc="B0C3361B" md5="6D24C94D3ACD89B4B703F7BD2A504833" sha1="BA839BEA8F76BF955E3EDF7083D2CBE780244ADD" status="verified"/>
    </game>
    <game name="Battletoads in Ragnarok's World (Europe)">
        <description>Battletoads in Ragnarok's World (Europe)</description>
        <rom name="Battletoads in Ragnarok's World (Europe).gb" size="131072" crc="7FFC34EA" md5="BC76C0516129C6791E4087F93F5D3C99" sha1="1852BD23644E28109B66FA937053C689A63F7729" status="verified"/>
    </game>
    <game name="Battletoads in Ragnarok's World (USA)">
        <description>Battletoads in Ragnarok's World (USA)</description>
        <rom name="Battletoads in Ragnarok's World (USA).gb" size="131072" crc="CE316C68" md5="4866EA7BDAA92C6986D4847209EBBD20" sha1="3DF1384E699B91689F015D7ABA65AB42410E24F5"/>
    </game>
</datafile>
""",
    header=dict(
        name='Nintendo - Game Boy',
        description='Nintendo - Game Boy',
        version='20171226-085946',
        author='C. V. Reynolds, Densetsu, xuom2',
        homepage='No-Intro',
        url='http://www.no-intro.org',
    ),
)


@pytest.mark.parametrize("test_data,expected", [
    (DAT_01['xml'], DAT_01['header']),
    (DAT_02['xml'], DAT_02['header']),
    (DAT_03['xml'], DAT_03['header']),
])
def test_load_sample_data(test_data, expected):
    with patch('xml.etree.ElementTree.open', mock_open(read_data=test_data)) as mock_file:
        dat = DatafileXml(PATH)

    mock_file.assert_called_with(PATH, ANY)
    assert dat.name == expected['name']
    assert dat.description == expected['description']
    assert dat.version == expected['version']
    assert dat.author == expected['author']
    assert dat.homepage == expected['homepage']
    assert dat.url == expected['url']
