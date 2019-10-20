from drugs_shooting_list.parser.load import load, EncyclopatiaParser


class TestEncylopatiaParser:
    parse = EncyclopatiaParser.parse_row

    def test_simple_row(self):
        key = 'Оциллококцинум'
        desc = 'у гомеопатии не может быть доказательств эффективности'
        row = f'<li>{key}: {desc}</li>'
        result = [key.lower()], desc
        assert self.parse(row) == result

    def test_simple_row_dash(self):
        key = 'АТФ-форте'
        key2 = 'Трифосаденин'
        row = f'<li>{key} — см. {key2}.</li>'
        result = [key.lower(), key2.lower()], None
        assert self.parse(row) == result

    def test_simple_row_with_sep(self):
        key = 'Оциллококцинум'
        desc = 'у гомеопатии не может быть доказательств эффективности'
        row = f'<li>{key} — {desc}</li>'
        result = [key.lower()], desc
        assert self.parse(row) == result, row

    def test_linked_desc(self):
        key1, key2 = 'Олифен', 'Гипоксен'
        row = f'<li>{key1} — см. {key2}.</li>'
        result = [key1.lower(), key2.lower()], None
        assert self.parse(row) == result, row

    def test_multiple_keys_simple(self):
        key1, key2 = 'Циннабсин', 'Cinnabsin'
        desc = 'у гомеопатии не может быть доказательств эффективности'
        row = f'<li>{key1} ({key2}): {desc}.</li>'
        result = [key1.lower(), key2.lower()], desc
        assert self.parse(row) == result, row

    def test_multiple_keys_slash_sep(self):
        key1, key2 = 'Циннабсин', 'Cinnabsin'
        desc = 'у гомеопатии не может быть доказательств эффективности'
        row = f'<li>{key1} ({key1}/{key2}): {desc}.</li>'
        result = [key1.lower(), key1.lower(), key2.lower()], desc
        assert self.parse(row) == result, row

    def test_key_with_slash_sep(self):
        key1, key2 = 'Циннабсин', 'Cinnabsin'
        desc = 'у гомеопатии не может быть доказательств эффективности'
        row = f'<li>{key1}/{key2}: {desc}.</li>'
        result = [key1.lower(), key2.lower()], desc
        assert self.parse(row) == result, row

    def test_custom_row(self):
        row = 'Анаферон: антитела к гамма интерферону человека аффинно' \
              ' очищенные – 0,003 г с содержанием не более 10−15 нг/г. ' \
              'Псевдопрепарат, который мимикрирует под псевдопрепарат: ' \
              'интерфероны при ОРВИ бесполезны (см. ниже)'
        keys, value = self.parse(row)
        assert keys == ['анаферон']
