#!/usr/bin/env python

import json
from xml.etree import ElementTree
from urllib import request

url = 'https://encyclopatia.ru/wiki/%D0%A0%D0%B0%D1%81%D1%81%D1%82%D1%80%D0%B5%D0%BB%D1%8C%D0%BD%D1%8B%D0%B9_%D1%81%D0%BF%D0%B8%D1%81%D0%BE%D0%BA_%D0%BF%D1%80%D0%B5%D0%BF%D0%B0%D1%80%D0%B0%D1%82%D0%BE%D0%B2'


class ParseError(Exception):
    pass


response = request.urlopen(url)

if response.code != 200:
    raise ParseError()

el = ElementTree.parse(response)

got_literal = False

results = {}

for el in el.getiterator():
    if got_literal:
        if el.tag == 'ul':
            for e in el.getchildren():
                if e.tag == 'li':
                    sep = ':' if ':' in e.text else '—'
                    key, _sep, value = e.text.partition(sep)
                    if key:
                        results[key] = value
                        print(e.text)
                    else:
                        print('Error ', e.text)

        got_literal = False
        continue

    if el.tag == 'span' and '.D0.' in el.get('id', '') and len(el.get('id', '')) < 20:
        got_literal = True
        continue
    got_literal = False

json.dump(results, open('results.json', 'w'))
