"""
[summary]

[extended_summary]
"""

# region [Imports]

# * Standard Library Imports ---------------------------------------------------------------------------->
import os

# * Gid Imports ----------------------------------------------------------------------------------------->
import gidlogger as glog

# endregion [Imports]


# region [TODO]


# endregion [TODO]

# region [AppUserData]


# endregion [AppUserData]

# region [Logging]

log = glog.aux_logger(__name__)
log.info(glog.imported(__name__))

# endregion[Logging]

# region [Constants]

THIS_FILE_DIR = os.path.abspath(os.path.dirname(__file__))

# endregion[Constants]

LOAD_ENV_SNIPPET = """
@echo off

rem ----------------------------------------------------------------
rem ##################### setting vars from $!$DEV_META_ENV_FILE_PATH$!$
for /f %%i in ($!$DEV_META_ENV_FILE_PATH$!$) do set %%i
rem ----------------------------------------------------------------

"""


# region[Main_Exec]

if __name__ == '__main__':
    pass

# endregion[Main_Exec]
