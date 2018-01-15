import os
import tempfile
from unittest.mock import patch, sentinel

import pytest
import toml

from srm.config import ChainConf, Conf, GlobalConf, LocalConf

# value for testing set/get
V = sentinel.V

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
    c['key'] = V
    assert c['key'] == V


def test_set_key_not_in_whitelist_raises_exception():
    c = Conf('cofig', valid_keys=['field_ok'])
    with pytest.raises(KeyError):
        c['field_bad'] = V


def test_set_and_del_key():
    c = Conf('config')
    c['key'] = V
    del c['key']
    with pytest.raises(KeyError):
        c['key']


def test_set_and_get_nested_key():
    c = Conf('config')
    c['s1.s2.key'] = V
    assert c['s1.s2.key'] == V


def test_set_and_del_nested_key():
    c = Conf('config')
    c['s1.s2.key'] = V
    del c['s1.s2.key']
    with pytest.raises(KeyError):
        c['s1.s2.key']


def test_dump_config():
    with tempfile.NamedTemporaryFile() as t:
        c = Conf(t.name)
        c['key'] = V
        c.dump()
        with open(t.name) as f:
            assert f.readline() == 'key = sentinel.V\n'


def test_dump_nested_config():
    with tempfile.NamedTemporaryFile() as t:
        c = Conf(t.name)
        c['s1.s2.key'] = V
        assert 's1.s2.key' in c
        c.dump()
        with open(t.name) as f:
            assert f.readlines() == ['[s1.s2]\n', 'key = sentinel.V\n']


def test_load_config():
    with tempfile.NamedTemporaryFile() as t:
        with open(t.name, 'w+') as f:
            toml.dump({'key1': 1, 'key2': 2}, f)
        c = Conf(t.name)
        c.load()
        assert 'key2' in c
        assert c['key2'] == 2


def test_dump_chain_config():
    with tempfile.NamedTemporaryFile() as t:
        c = ChainConf(Conf(t.name))
        c['key'] = V
        c.dump()
        with open(t.name) as f:
            assert f.readline() == 'key = sentinel.V\n'


def test_load_chain_config():
    with tempfile.NamedTemporaryFile() as t:
        with open(t.name, 'w+') as f:
            toml.dump({'key1': 1, 'key2': 2}, f)
        c = ChainConf(Conf(t.name))
        c.load()
        assert 'key2' in c
        assert c['key2'] == 2


def test_get_global_key_from_chain_config():
    with tempfile.NamedTemporaryFile() as global_path:
        # set a key/value into mock global config
        gconf = Conf(global_path.name)
        gconf['key'] = 1
        gconf.dump()
        # test
        with tempfile.NamedTemporaryFile() as local_path:
            c = ChainConf(Conf(local_path.name), gconf)
            c.load()
            assert 'key' in c
            assert c['key'] == 1

def test_chain_config_exists():
    with tempfile.NamedTemporaryFile() as t:
        c = ChainConf(Conf(t.name))
        assert c.exists()
