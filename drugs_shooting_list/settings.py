import os
from runpy import run_path


local_settings = os.environ.copy()

local_settings_file = local_settings.get('LOCAL_SETTINGS_FILE') or '.local_settings.py'

if os.path.exists(local_settings_file):
    local_settings = run_path(local_settings_file)

TOKEN = local_settings.get('TOKEN')
DATA_FILE_PATH = local_settings.get('DATA_FILE_PATH') or 'results.json'
