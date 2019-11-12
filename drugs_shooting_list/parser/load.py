#!/usr/bin/env python

import json
import xml.etree.ElementTree as ET
from dataclasses import dataclass
from html import unescape
from urllib import request
from urllib.error import HTTPError


encyclopatia_url = 'https://encyclopatia.ru/wiki/%D0%A0%D0%B0%D1%81%D1%81%D1%82%D1%80%D0%B5%D0%BB%D1%8C%D0%BD%D1%8B%D0%B9_%D1%81%D0%BF%D0%B8%D1%81%D0%BE%D0%BA_%D0%BF%D1%80%D0%B5%D0%BF%D0%B0%D1%80%D0%B0%D1%82%D0%BE%D0%B2'
rlsnet_url_template = 'https://www.rlsnet.ru/tn_alf_letter_{page}.htm'


class ParseError(Exception):
    pass

@dataclass
class DrugDescription:
    alter_keys: list
    description: str or None
    is_shooting: bool

    def data(self):
        return self.__dict__


def get_data(url):
    try:
        response = request.urlopen(url)
    except HTTPError as e:
        if e.code == 404:
            print(f'Page not found {url}')
            return b''
        raise

    if response.code == 200:
        return response.read()

    raise ParseError(response)


class EncyclopatiaParser:
    base_url = 'https://encyclopatia.ru'

    started = False
    start_tag = '<h2><span class="mw-headline" id=".D0.90">А</span></h2>'
    end_tag = '<h2><span class="mw-headline" id=".D0.95.D1.89.D1.91">Ещё</span></h2>'

    def __init__(self, data=None) -> None:
        super().__init__()
        self._data = data.decode().splitlines()
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
        return keys, description, True

    @classmethod
    def normalize_html_to_tg(cls, html):
        result = html
        forbidden_tags = (
            'i',
            'del',
            'span',
        )
        result = result.replace('href="/', f'href="{cls.base_url}/')
        for tag in forbidden_tags:
            result = result.replace(f'<{tag}>', '')  # <tag>
            result = result.replace(f'</{tag}>', '')  # </tag>
        return result


class RLSNETParser:
    started = False
    start_tag = '</div></div><div xmlns:php="http://php.net/xsl" class="tn_alf_list"><ul>'
    end_tag= '<div class="alphabet__delimiter"><span class="alphabet__letters">'

    encoding = 'windows-1251'

    def __init__(self, data=None) -> None:
        super().__init__()
        self._data = data.decode(self.encoding).splitlines()
        self._data.reverse()

    def __iter__(self):
        return self

    def __next__(self):
        if not self._data:
            raise StopIteration()

        row = self._data.pop()
        if row == self.end_tag:
            raise StopIteration()

        if row == self.start_tag:
            self.started = True
            return next(self)

        if not self.started:
            return next(self)

        if '<li><a href=' not in row:
            return next(self)

        try:
            return self.parse_row(row)
        except ValueError as e:
            print(e)
            return next(self)

    @classmethod
    def parse_row(cls, row):
        row = unescape(row)
        row = row.replace('&alpha;', 'α')
        row = row.replace('&', '')

        parser = ET.XMLParser(encoding=cls.encoding)
        et = ET.fromstring(row, parser=parser)

        a_tag = et[0]
        if a_tag.tag != 'a':
            raise ParseError(row)

        keys = []
        text = a_tag.text
        if text:
           keys.append(text.strip().lower())

        for inner_key in a_tag:
            alter_key = inner_key.text.strip('(®)').lower()
            if alter_key:
                keys.append(alter_key)

            for inner_alter_key in inner_key:
                if inner_alter_key.tag == 'i':
                    keys.append(inner_alter_key.text.strip('(®)').lower())

        description = a_tag.get('href').lstrip('/')
        keys = [
            k.replace('<sup>®</sup>', ' ') for k in keys
        ]
        return keys, description, False

    @classmethod
    def normalize_html_to_tg(cls, html):
        result = html
        forbidden_tags = (
            'i',
            'del',
            'span',
        )
        for tag in forbidden_tags:
            result = result.replace(f'<{tag}>', '')  # <tag>
            result = result.replace(f'</{tag}>', '')  # </tag>
        return result


parsers = (
    (RLSNETParser, rlsnet_url_template,
        (hex(x)[2:] for x in list(range(0xc0, 0xe0))+[1])),
    (EncyclopatiaParser, encyclopatia_url, (None, )),
)


def load():
    results = {}
    for parser, url, pages in parsers:
        for page in pages:
            data = get_data(url.format(page=page))
            for data in parser(data):
                (key, *alter_keys), value, is_shooting = data

                value = value and parser.normalize_html_to_tg(value)

                if key in results:
                    old_desc = results[key]
                    results[key] = DrugDescription(
                        alter_keys + old_desc.alter_keys,
                        value or old_desc.description,
                        old_desc.is_shooting
                    )
                else:
                    results[key] = DrugDescription(
                        alter_keys=alter_keys,
                        description=value,
                        is_shooting=is_shooting,
                    )

                for alter_key in alter_keys:
                    if alter_key not in results:
                        results[alter_key] = DrugDescription(
                            alter_keys=[key],
                            description=None,
                            is_shooting=is_shooting,
                    )
    return results


def dump(results, file_name):
    json_results = [
        (k, v.data()) for k,v in results.items()
    ]
    json.dump(json_results, open(file_name, 'w'))


if __name__ == '__main__':
    dump(load(), 'results.json')
