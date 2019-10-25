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
    base_url = 'https://encyclopatia.ru'

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

        for current_sep in (':', ' — ', ' - '):
            key, sep,  description = row.partition(current_sep)
            if sep:
                break
        else:
            raise ValueError(f'Unrecognized row: {row}')

        key = key.strip()
        description = description.strip().strip('.')
        keys = []
        if '(' in key:
            key, _keys = key.split('(', 1)
            splited = _keys.split('/')
            if len(splited) == 1:
                splited = _keys.split(',')
            keys = key.split('/') + splited

        if '/' in key:
            keys += key.split('/')
        else:
            keys = keys or key.split()

        if description.strip().startswith('см.'):
            keys.append(description.replace('см.', ''))
            description = None
        else:
            description = row.strip('</>lui')

        keys = [x.lower().strip('(').strip(')') for x in keys]
        keys = [x.replace('—', '') for x in keys]
        keys = [x.replace('и пр.', '') for x in keys]
        keys = [x.strip() for x in keys]
        return keys, description

    @classmethod
    def normalize_html_to_tg(cls, html):
        return html.replace(
            '<del>', '<i>'
        ).replace(
            '</del>', '</i>'
        ).replace(
            'href="/', f'href="{cls.base_url}/')


def load(data):
    results = {}
    for data in EncyclopatiaParser(data):
        (key, *alter_keys), value = data

        value = value and EncyclopatiaParser.normalize_html_to_tg(value)

        if key in results:
            cur_alter_keys, old_value = results[key]
            new_value = value or old_value
            results[key] = alter_keys+cur_alter_keys, new_value
        else:
            results[key] = alter_keys, value

        for alter_key in alter_keys:
            if alter_key not in results:
                results[alter_key] = [key], None
    return results


def dump(results):
    json.dump(results, open('results.json', 'w'))


if __name__ == '__main__':
    dump(load(get_data(url)))
