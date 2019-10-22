import json
import os

from functools import wraps
from telegram import Update

from drugs_shooting_list.settings import DATA_FILE_PATH


class Data:
    _data = None

    def load(self, json_path=DATA_FILE_PATH):
        self._data = json.load(open(os.path.expandvars(json_path)))

    def get(self, key, not_found_message, processed_keys=None):
        if not self._data:
            self.load()
        result = not_found_message
        key = key.lower()
        processed_keys = processed_keys or [key]
        if key in self._data:
            keys, value = self._data.get(key)
            if value:
                result = value
            elif keys:
                for cur_key in keys:
                    if cur_key in processed_keys:
                        continue

                    value = DATA.get(cur_key, None, processed_keys)
                    processed_keys.append(cur_key)
                    if value:
                        result = value
                        break
        return result


DATA = Data()


def to_tg_update(bot):
    def wrapped(fn):
        @wraps(fn)
        def inner(event, *args, **kwargs):
            update = Update.de_json(json.loads(event.get('body')), bot)
            return fn(update, *args, **kwargs)
        return inner
    return wrapped


def get_drug_info(drug: str, not_found_message: str = 'Не найдено'):
    """Retrieve info by drug name

    :param drug: drug name
    :param not_found_message: return message for not found rows
    :return: info about drug
    """
    return DATA.get(drug, not_found_message)
