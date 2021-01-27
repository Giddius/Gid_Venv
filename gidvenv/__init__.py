"""
Custom Venv builder.
"""

__version__ = "0.1.0"


# region [Imports]

import appdirs
import os
from importlib.metadata import metadata
import gidlogger as glog
# endregion[Imports]


APP_NAME = metadata(__name__).get('name')
AUTHOR_NAME = metadata(__name__).get('author')
os.environ['APP_NAME'] = APP_NAME
os.environ["AUTHOR_NAME"] = AUTHOR_NAME


if os.getenv('USER_DATA_STORAGE_DIR', default=None) is None:

    USER_DATA_STORAGE_DIR = appdirs.user_data_dir(appname=APP_NAME, appauthor=AUTHOR_NAME, roaming=True)

    os.environ['USER_DATA_STORAGE_DIR'] = USER_DATA_STORAGE_DIR

if os.path.isdir(os.getenv('USER_DATA_STORAGE_DIR')) is False:
    os.makedirs(os.getenv('USER_DATA_STORAGE_DIR'))


_log_file = glog.log_folderer(APP_NAME)
_log = glog.main_logger(_log_file, 'debug', other_logger_names=[], log_to='stdout')
