"""
Custom Venv builder.
"""

__version__ = "0.1.0"

import colorama
import appdirs
import os
from importlib.metadata import metadata


colorama.init(autoreset=True)

APP_NAME = metadata(__name__).get('name')
AUTHOR_NAME = metadata(__name__).get('author')

if os.getenv('USER_DATA_STORAGE_DIR', default=None) is None:

    USER_DATA_STORAGE_DIR = appdirs.user_data_dir(appname=APP_NAME, appauthor=AUTHOR_NAME, roaming=True)

    os.environ['USER_DATA_STORAGE_DIR'] = USER_DATA_STORAGE_DIR

if os.path.isdir(os.getenv('USER_DATA_STORAGE_DIR')) is False:
    os.makedirs(os.getenv('USER_DATA_STORAGE_DIR'))
