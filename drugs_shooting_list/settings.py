import os
from runpy import run_path


local_settings = os.environ.copy()

local_settings_file = local_settings.get('LOCAL_SETTINGS_FILE') or '.local_settings.py'

if os.path.exists(local_settings_file):
    local_settings = run_path(local_settings_file)

TOKEN = local_settings.get('TOKEN')
PROXY = local_settings.get('PROXY')
ADMIN_UID = int(local_settings.get('ADMIN_UID', 0))
INLINE_QUERY_LEN = int(local_settings.get('INLINE_QUERY_LEN', 3))
INLINE_QUERY_COUNT = int(local_settings.get('INLINE_QUERY_COUNT', 6))
DATA_FILE_PATH = local_settings.get('DATA_FILE_PATH') or 'results.json'
