from drugs_shooting_list.parser.load import EncyclopatiaParser, RLSNETParser


class TestEncylopatiaParser:
    parse = EncyclopatiaParser.parse_row

    def test_simple_row(self):
        key = 'Оциллококцинум'
        desc = 'у гомеопатии не может быть доказательств эффективности'
        row = f'<li>{key}: {desc}</li>'
        result = [key.lower()], f'{key}: {desc}', True
        assert self.parse(row) == result

    def test_simple_row_dash(self):
        key = 'АТФ-форте'
        key2 = 'Трифосаденин'
        row = f'<li>{key} — см. {key2}.</li>'
        result = [key.lower(), key2.lower()], None, True
        assert self.parse(row) == result

    def test_simple_row_with_sep(self):
        key = 'Оциллококцинум'
        desc = 'у гомеопатии не может быть доказательств эффективности'
        row = f'<li>{key} — {desc}</li>'
        result = [key.lower()], f'{key} — {desc}', True
        assert self.parse(row) == result, row

    def test_linked_desc(self):
        key1, key2 = 'Олифен', 'Гипоксен'
        row = f'<li>{key1} — см. {key2}.</li>'
        result = [key1.lower(), key2.lower()], None, True
        assert self.parse(row) == result, row

    def test_multiple_keys_simple(self):
        key1, key2 = 'Циннабсин', 'Cinnabsin'
        desc = 'у гомеопатии не может быть доказательств эффективности'
        row = f'<li>{key1} ({key2}): {desc}.</li>'
        result = [key1.lower(), key2.lower()], f'{key1} ({key2}): {desc}.', True
        assert self.parse(row) == result, row

    def test_multiple_keys_slash_sep(self):
        key1, key2 = 'Циннабсин', 'Cinnabsin'
        desc = 'у гомеопатии не может быть доказательств эффективности'
        row = f'<li>{key1} ({key1}/{key2}): {desc}.</li>'
        result = [key1.lower(), key1.lower(), key2.lower()], \
                 f'{key1} ({key1}/{key2}): {desc}.', True
        assert self.parse(row) == result, row

    def test_key_with_slash_sep(self):
        key1, key2 = 'Циннабсин', 'Cinnabsin'
        desc = 'у гомеопатии не может быть доказательств эффективности'
        row = f'<li>{key1}/{key2}: {desc}.</li>'
        result = [key1.lower(), key2.lower()], f'{key1}/{key2}: {desc}.', True
        assert self.parse(row) == result, row

    def test_custom_row(self):
        row = 'Анаферон: антитела к гамма интерферону человека аффинно' \
              ' очищенные – 0,003 г с содержанием не более 10−15 нг/г. ' \
              'Псевдопрепарат, который мимикрирует под псевдопрепарат: ' \
              'интерфероны при ОРВИ бесполезны (см. ниже)'
        keys, value, _shoot = self.parse(row)
        assert keys == ['анаферон']

    def test_key_strip(self):
        key = 'Дибазол'
        row = f'{key} — (Dibazol/Bendazole): препарат из СССР для'
        keys, value, _shoot = self.parse(row)
        assert keys[0] == key.lower()

    def test_key_strip2(self):
        key = 'Расторопша'
        key2 = 'пятнистая'
        row = f'{key} {key2}: фитотерапия для печени'
        keys, value, _shoot = self.parse(row)
        assert keys == [key.lower(), key2]

    def test_key_strip3(self):
        expected_keys = [
            'Спреи с антибиотиками', 'антисептиками при рините', 'Изофра',
            'Полидекса', 'Биопарокс', 'Мирамистин'
        ]
        value = 'применение местных антибиотиков в носу бессмысленно'

        row = f'Спреи с антибиотиками/антисептиками при рините (Изофра,' \
              f' Полидекса, Биопарокс, Мирамистин и пр.) — {value}'

        keys, value, _shoot = self.parse(row)
        # FIXME
        assert keys == [x.lower() for x in expected_keys] + ['спреи с антибиотиками', 'антисептиками при рините']
        assert value == row

    def test_key_strip4(self):
        row = 'Иммунал (Иммунорм/Immunal): фитотерапевтический иммуномодулятор для профилактики ОРВИ и «укрепления» иммунитета — см. Эхинацея. Cochrane Reviews 0; Pubmed 0; FDA 0; RXlist 0; ВОЗ 0; ФК (-).'

        keys, value, _shoot = self.parse(row)

        assert keys == ['иммунал', 'иммунорм', 'immunal']
        assert value == row


class TestRLSNETParser:
    parse = RLSNETParser.parse_row

    def test_parse_simple(self):
        row = '<li><a href="//www.rlsnet.ru/tn_index_id_70623.htm">Абаджио</a> </li>'
        keys, value, _shoot = self.parse(row)

        assert keys == ['абаджио']
        assert value == 'www.rlsnet.ru/tn_index_id_70623.htm'

    def test_parse_simple_with_trade_mark(self):
        row = '<li><a href="//www.rlsnet.ru/tn_index_id_70623.htm">Абаджио<sup>®</sup></a> </li>'
        keys, value, _shoot = self.parse(row)

        assert keys == ['абаджио']
        assert value == 'www.rlsnet.ru/tn_index_id_70623.htm'

    def test_parse_row_with_alter_key(self):
        row = '<li><a href="//www.rlsnet.ru/tn_index_id_98587.htm">Абакавир + Зидовудин + Ламивудин <i>(Abacavir +  Zidovudine + Lamivudine)</i></a> </li>'
        keys, value, _shoot = self.parse(row)

        assert keys == ['абакавир + зидовудин + ламивудин', 'abacavir +  zidovudine + lamivudine']
        assert value == 'www.rlsnet.ru/tn_index_id_98587.htm'

    def test_parse_bold_key(self):
        row = '<li><a href="//www.rlsnet.ru/tn_index_id_67009.htm"><b>Авиамарин<sup>®</sup> <i>(Aviamarin)</i></b></a> <span class="zvezdaElem"></span><a href="/tn_index_id_67009.htm#ceny-v-aptekax-moskvy"><span class="monetkaElem"></span></a><span class="descElem"></span><span class="imgElem"></span></li>'
        keys, value, _shoot = self.parse(row)

        assert keys == ['авиамарин', 'aviamarin']
        assert value == 'www.rlsnet.ru/tn_index_id_67009.htm'

    def test_parse_row_with_a_char(self):
        row = '<li><a href="//www.rlsnet.ru/tn_index_id_48702.htm">Иматиниба мезилат &alpha;-форма <i>(Iimatinib mesilate)</i></a> <span class="zvezdaElem"></span></li>'
        keys, value, _shoot = self.parse(row)

        assert keys == ['иматиниба мезилат α-форма', 'iimatinib mesilate']
        assert value == 'www.rlsnet.ru/tn_index_id_48702.htm'

    def test_parse_with_at_char(self):
        row = '<li><a href="//www.rlsnet.ru/tn_index_id_16804.htm">Растворы ЦФГ и С.А.Г.М. «Теруфлекс» <i>(Solutions CDP & S.A.G.M. &#171;Teruflex&#187;)</i></a> </li>'
        keys, value, _shoot = self.parse(row)

        assert keys == ['растворы цфг и с.а.г.м. «теруфлекс»',
                        'solutions cdp  s.a.g.m. «teruflex»']
        assert value == 'www.rlsnet.ru/tn_index_id_16804.htm'
