
# region [Imports]

# * Standard Library Imports ---------------------------------------------------------------------------->
import os
import sys
import logging

# * Third Party Imports --------------------------------------------------------------------------------->
import click

# * Gid Imports ----------------------------------------------------------------------------------------->
import gidlogger as glog

# * Local Imports --------------------------------------------------------------------------------------->
from gidvenv.utility.gidfiles_functions import pathmaker
from gidvenv import APP_NAME

# endregion [Imports]


# region [Logging]
_log_file = glog.log_folderer(APP_NAME)
log = glog.main_logger(_log_file, 'debug', other_logger_names=[], log_to='stdout')


# endregion[Logging]

log.info('starting Gidvenv tool')
