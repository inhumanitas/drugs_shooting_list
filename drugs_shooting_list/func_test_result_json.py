import sys

from drugs_shooting_list.utils import DATA, get_drug_info


DATA.load('results.json')
data = DATA._data


def test_keys(data):
    assert data
    result = 0
    for key in data:
        try:
            text = get_drug_info(key)
        except RecursionError:
            print(key)
            result = 1
        try:
            assert text
        except AssertionError:
            print(f'Empty value for key - {key}')
            result = 1
    return result


sys.exit(test_keys(data))
