import json

from functools import wraps
from telegram import Update

from drugs_shooting_list.settings import DATA_FILE_PATH

_data = None


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
    global _data
    if _data is None:
        _data = json.load(open(DATA_FILE_PATH))
    return _data.get(drug, not_found_message)
