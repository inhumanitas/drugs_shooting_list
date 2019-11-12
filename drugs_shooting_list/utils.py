import difflib
import json
import os
from dataclasses import dataclass

from functools import wraps

from drugs_shooting_list.settings import DATA_FILE_PATH, INLINE_QUERY_LEN, \
    INLINE_QUERY_COUNT


@dataclass
class DrugDescription:
    alter_keys: list
    description: str or None
    is_shooting: bool

    def data(self):
        return self.__dict__


class Data:
    _data = None

    @property
    def data(self):
        if self._data is None:
            self.load()
        return self._data

    @property
    def keys(self):
        return self.data.keys() if self.data else []

    def load(self, json_path=DATA_FILE_PATH):
        raw = json.load(open(os.path.expandvars(json_path)))
        self._data = {}
        for k, data in raw:
            self._data[k] = DrugDescription(**data)

    def get(self, key, default_value, processed_keys=None):
        result = default_value
        key = key.lower()
        processed_keys = processed_keys or [key]
        if key in self.data:
            drug_description = self.data.get(key)
            if drug_description.description:
                result = drug_description.description
            elif drug_description.alter_keys:
                for cur_key in drug_description.alter_keys:
                    if cur_key in processed_keys:
                        continue

                    description = self.get(cur_key, None, processed_keys)
                    processed_keys.append(cur_key)
                    if description:
                        result = description
                        break
        return result

    def get_subkeys(self, substr):
        """Find the keys that are starts with `substr`
        :param substr: key substring
        :return first N values that starts with `substr` or [] if not found
        """
        result = []
        if len(substr) >= INLINE_QUERY_LEN:
            for key in self.keys:
                if len(result) >= INLINE_QUERY_COUNT:
                    break

                if key.startswith(substr):
                    result.append(key)
        return result


DATA = Data()


def to_tg_update(bot):
    from telegram import Update

    def wrapped(fn):
        @wraps(fn)
        def inner(event, *args, **kwargs):
            update = Update.de_json(json.loads(event.get('body')), bot)
            return fn(update, *args, **kwargs)
        return inner
    return wrapped


def get_drug_info(drug: str, default_value=None):
    """Retrieve info by drug name

    :param drug: drug name
    :param default_value: value for not found rows
    :return: info about drug
    """
    return DATA.get(drug, default_value)


def predict_key(key, words=1):
    return difflib.get_close_matches(key, DATA.keys, words, 0)
