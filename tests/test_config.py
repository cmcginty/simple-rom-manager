import os
import tempfile
import unittest.mock

import pytest
import toml

from srm.config import Conf, GlobalConf, LocalConf


def test_config_not_exists():
    with tempfile.TemporaryDirectory() as d:
        c = Conf(d)
        assert not c.exists()


def test_config_exists():
    with tempfile.NamedTemporaryFile() as t:
        c = Conf(t.name)
        assert c.exists()


def test_load_create_with_path():
    with tempfile.TemporaryDirectory() as d:
        c = Conf(os.path.join(d, "a/b/file.txt"))
        c.load(create=True)
        assert c.exists()


def test_set_and_get_key():
    c = Conf('cofig')
    c['key'] = 10
    assert c['key'] == 10


def test_set_key_not_in_whitelist_raises_exception():
    c = Conf('cofig', valid_keys=['field_ok'])
    with pytest.raises(KeyError):
        c['field_bad'] = 10


def test_set_and_del_key():
    c = Conf('config')
    c['key'] = 10
    del c['key']
    with pytest.raises(KeyError):
        c['key']


def test_set_and_get_nested_key():
    c = Conf('config')
    c['s1.s2.key'] = 10
    assert c['s1.s2.key'] == 10


def test_set_and_del_nested_key():
    c = Conf('config')
    c['s1.s2.key'] = 10
    del c['s1.s2.key']
    with pytest.raises(KeyError):
        c['s1.s2.key']


def test_dump_config():
    with tempfile.NamedTemporaryFile() as t:
        c = Conf(t.name)
        c['key'] = 10
        c.dump()
        with open(t.name) as f:
            assert f.readline() == 'key = 10\n'


def test_dump_nested_config():
    with tempfile.NamedTemporaryFile() as t:
        c = Conf(t.name)
        c['s1.s2.key'] = 10
        assert 's1.s2.key' in c
        c.dump()
        with open(t.name) as f:
            assert f.readlines() == ['[s1.s2]\n', 'key = 10\n']


def test_load_config():
    with tempfile.NamedTemporaryFile() as t:
        with open(t.name, 'w+') as f:
            toml.dump({'key1': 1, 'key2': 2}, f)
        c = Conf(t.name)
        c.load()
        assert 'key2' in c
        assert c['key2'] == 2


def test_dump_local_config():
    with tempfile.NamedTemporaryFile() as t:
        c = LocalConf(t.name)
        c['key'] = 10
        c.dump()
        with open(t.name) as f:
            assert f.readline() == 'key = 10\n'


def test_load_local_config():
    with tempfile.NamedTemporaryFile() as t:
        with open(t.name, 'w+') as f:
            toml.dump({'key1': 1, 'key2': 2}, f)
        c = LocalConf(t.name)
        c.load()
        assert 'key2' in c
        assert c['key2'] == 2


@unittest.mock.patch('srm.config.GlobalConf', autospec=True)
def test_get_global_key_from_local_config(gconf_cls):
    with tempfile.NamedTemporaryFile() as global_path:
        # set a key/value into mock global config
        gconf = Conf(global_path.name)
        gconf_cls.return_value = gconf
        gconf['key'] = 10
        gconf.dump()
        # test
        with tempfile.NamedTemporaryFile() as local_path:
            c = LocalConf(local_path.name)
            c.load()
            assert 'key' in c
            assert c['key'] == 10
