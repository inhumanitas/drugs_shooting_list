from drugs_shooting_list import utils

data = {
    'key1': ([], 'value1'),
    'key2': (['key1'], None),
    'key3': (['key2'], None),
    'key4': ([], None),
    'key5': ([], ''),
    'key6': (['key7'], 'value6'),
    # 'key6': (['key6'], None), ???
}

utils.DATA._data = data


def test_get_drug_data():
    assert utils.get_drug_info('key1') == data['key1'][1]


def test_get_drug_data_no_key():
    no_key = 'empty'
    assert utils.get_drug_info(no_key, not_found_message=no_key) == no_key


def test_linked_get():
    key = 'key2'
    value = data['key1'][1]
    assert utils.get_drug_info(key) == value
    key = 'key3'
    assert utils.get_drug_info(key) == value


def test_empty_get():
    keys = ('key4', 'key5', '__key__')
    value = 'empty'
    for key in keys:
        assert utils.get_drug_info(key, not_found_message=value) == value
