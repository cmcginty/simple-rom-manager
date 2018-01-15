"""
Test cases for file operations.
"""

import tempfile

from srm.file import Path


def test_path_calculates_hashes():
    with tempfile.NamedTemporaryFile(delete=False) as f:
        f.write(b'The quick brown fox jumps over the lazy dog')
        f.close()
        p = Path(f.name)
        assert p.crc() == '414fa339'
        assert p.md5() == '9e107d9d372bb6826bd81d3542a419d6'
        assert p.sha1() == '2fd4e1c67a2d28fced849ee1bb76e7391b93eb12'
        p.unlink()
