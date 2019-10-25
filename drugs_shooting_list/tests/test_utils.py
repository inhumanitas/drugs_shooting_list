import pytest

from drugs_shooting_list import utils


@pytest.fixture()
def data():
    data = {
        'key1': ([], 'value1'),
        'key2': (['key1'], None),
        'key3': (['key2'], None),
        'key4': ([], None),
        'key5': ([], ''),
        'key6': (['key7'], 'value6'),
        'key7': (['key8', 'key6'], None),
        'key8': (['key7'], None),
    }

    utils.DATA._data = data
    return data


def test_get_drug_data(data):
    assert utils.get_drug_info('key1') == data['key1'][1]


def test_get_drug_data_no_key():
    no_key = 'empty'
    assert utils.get_drug_info(no_key, default_value=no_key) == no_key


def test_linked_get(data):
    key = 'key2'
    value = data['key1'][1]
    assert utils.get_drug_info(key) == value
    key = 'key3'
    assert utils.get_drug_info(key) == value


def test_empty_get():
    keys = ('key4', 'key5', '__key__')
    value = 'empty'
    for key in keys:
        assert utils.get_drug_info(key, default_value=value) == value


def test_recursive_keys(data):
    key = 'key7'
    assert utils.get_drug_info(key) == data['key6'][1]
