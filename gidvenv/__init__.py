"""
Custom Venv builder.
"""

__version__ = "0.1.0"


def make_title(parts):
    return ''.join(map(lambda x: x.title(), parts))


_app_name_parts = ("gid", "venv")
_author_name_parts = ("broca", "progs")

APP_NAME_LOWER = ''.join(_app_name_parts)
AUTHOR_NAME_LOWER = ''.join(_author_name_parts)

APP_NAME_UPPER = APP_NAME_LOWER.upper()
AUTHOR_NAME_UPPER = AUTHOR_NAME_LOWER.upper()

APP_NAME_TITLE = make_title(_app_name_parts)
AUTHOR_NAME_TITLE = make_title(_author_name_parts)

APP_NAME = APP_NAME_LOWER
AUTHOR_NAME = AUTHOR_NAME_LOWER

# region [Imports]
import os
import appdirs
import gidlogger as glog

# endregion[Imports]


appdata_dir = appdirs.user_data_dir(appname=APP_NAME_TITLE, appauthor=AUTHOR_NAME_TITLE, roaming=True,)

if os.path.isdir(appdata_dir) is False:
    os.makedirs(appdata_dir)

# if os.getenv('IS_TEST', '0').casefold() != '1':
#     _log_file = glog.log_folderer(APP_NAME)
#     _log = glog.main_logger(_log_file, 'debug', other_logger_names=[], log_to='stdout')
