import tempfile

from srm.config import Conf


def test_config_exists():
    with tempfile.TemporaryDirectory() as d:
        c = Conf(d)
        assert not c.exists()

    with tempfile.NamedTemporaryFile() as t:
        c = Conf(t.name)
        assert c.exists()
