import pytest

from drugs_shooting_list import utils


@pytest.fixture()
def data():
    data = {
        'key1': utils.DrugDescription([], 'value1', False),
        'key2': utils.DrugDescription(['key1'], None, False),
        'key3': utils.DrugDescription(['key2'], None, False),
        'key4': utils.DrugDescription([], None, False),
        'key5': utils.DrugDescription([], '', False),
        'key6': utils.DrugDescription(['key7'], 'value6', False),
        'key7': utils.DrugDescription(['key8', 'key6'], None, False),
        'key8': utils.DrugDescription(['key7'], None, False),
    }

    utils.DATA._data = data
    return data


def test_get_drug_data(data):
    assert utils.get_drug_info('key1') == data['key1'].description


def test_get_drug_data_no_key():
    no_key = 'empty'
    assert utils.get_drug_info(no_key, default_value=no_key) == no_key


def test_linked_get(data):
    key = 'key2'
    value = data['key1'].description
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
    assert utils.get_drug_info(key) == data['key6'].description
