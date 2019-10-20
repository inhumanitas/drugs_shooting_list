#!/usr/bin/env python

import json
from urllib import request

url = 'https://encyclopatia.ru/wiki/%D0%A0%D0%B0%D1%81%D1%81%D1%82%D1%80%D0%B5%D0%BB%D1%8C%D0%BD%D1%8B%D0%B9_%D1%81%D0%BF%D0%B8%D1%81%D0%BE%D0%BA_%D0%BF%D1%80%D0%B5%D0%BF%D0%B0%D1%80%D0%B0%D1%82%D0%BE%D0%B2'


class ParseError(Exception):
    pass


def get_data(url):
    response = request.urlopen(url)

    if response.code != 200:
        raise ParseError()
    return response.read().decode()


class EncyclopatiaParser:
    started = False
    start_tag = '<h2><span class="mw-headline" id=".D0.90">А</span></h2>'
    end_tag = '<h2><span class="mw-headline" id=".D0.95.D1.89.D1.91">Ещё</span></h2>'

    def __init__(self, data=None) -> None:
        super().__init__()
        self._data = data.splitlines()
        self._data.reverse()

    def __iter__(self):
        return self

    def __next__(self):
        row = self._data.pop()
        if row == self.end_tag:
            raise StopIteration()

        if row == self.start_tag:
            self.started = True
            return next(self)

        if not self.started:
            return next(self)

        if '<li>' not in row:
            return next(self)

        try:
            return self.parse_row(row)
        except ValueError as e:
            print(e)
            return next(self)

    @classmethod
    def parse_row(cls, row):
        row = row.rstrip('<>uli')
        row = row.strip('</>uli')

        for current_sep in (':', ' - ', ' — '):
            key, sep,  description = row.partition(current_sep)
            if sep:
                break
        else:
            raise ValueError(f'Unrecognized row: {row}')

        key = key.strip()
        description = description.strip().strip('.')

        if '(' in key:
            head, _keys = key.split('(', 1)
            keys = [head] + _keys.split('/')
        elif '/' in key:
            keys = key.split('/')
        else:
            keys = [key]

        if description.strip().startswith('см.'):
            keys.append(description.strip('см.'))
            description = None

        keys = list(
            map(
                lambda x: x.strip().strip('(').strip(')').lower(),
                keys
            )
        )
        return keys, description


def load(data):
    results = {}
    for data in EncyclopatiaParser(data):
        (key, *other_keys), value = data
        results[key] = other_keys, value
    return results


def dump(results):
    json.dump(results, open('results.json', 'w'))


if __name__ == '__main__':
    dump(load(get_data(url)))
