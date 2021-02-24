"""
[summary]

[extended_summary]
"""

# region [Imports]

# * Standard Library Imports ------------------------------------------------------------------------------------------------------------------------------------>

import gc
import os
import re
import sys
import json
import lzma
import time
import queue
import base64
import pickle
import random
import shelve
import shutil
import asyncio
import logging
import sqlite3
import platform
import importlib
import subprocess
import unicodedata

from io import BytesIO
from abc import ABC, abstractmethod
from copy import copy, deepcopy
from enum import Enum, Flag, auto
from time import time, sleep
from pprint import pprint, pformat
from string import Formatter, digits, printable, whitespace, punctuation, ascii_letters, ascii_lowercase, ascii_uppercase
from timeit import Timer
from typing import Union, Callable, Iterable
from inspect import stack, getdoc, getmodule, getsource, getmembers, getmodulename, getsourcefile, getfullargspec, getsourcelines
from zipfile import ZipFile
from datetime import tzinfo, datetime, timezone, timedelta
from tempfile import TemporaryDirectory
from textwrap import TextWrapper, fill, wrap, dedent, indent, shorten
from functools import wraps, partial, lru_cache, singledispatch, total_ordering
from importlib import import_module, invalidate_caches
from contextlib import contextmanager
from statistics import mean, mode, stdev, median, variance, pvariance, harmonic_mean, median_grouped
from collections import Counter, ChainMap, deque, namedtuple, defaultdict
from urllib.parse import urlparse
from importlib.util import find_spec, module_from_spec, spec_from_file_location
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor
from importlib.machinery import SourceFileLoader
from functools import singledispatchmethod, singledispatch

# * Third Party Imports ----------------------------------------------------------------------------------------------------------------------------------------->

# import discord

# import requests

# import pyperclip

# import matplotlib.pyplot as plt

# from bs4 import BeautifulSoup

# from dotenv import load_dotenv

# from discord import Embed, File

# from discord.ext import commands, tasks

# from github import Github, GithubException

# from jinja2 import BaseLoader, Environment

# from natsort import natsorted

# from fuzzywuzzy import fuzz, process


# * PyQt5 Imports ----------------------------------------------------------------------------------------------------------------------------------------------->

# from PyQt5.QtGui import QFont, QIcon, QBrush, QColor, QCursor, QPixmap, QStandardItem, QRegExpValidator

# from PyQt5.QtCore import (Qt, QRect, QSize, QObject, QRegExp, QThread, QMetaObject, QCoreApplication,
#                           QFileSystemWatcher, QPropertyAnimation, QAbstractTableModel, pyqtSlot, pyqtSignal)

# from PyQt5.QtWidgets import (QMenu, QFrame, QLabel, QAction, QDialog, QLayout, QWidget, QWizard, QMenuBar, QSpinBox, QCheckBox, QComboBox, QGroupBox, QLineEdit,
#                              QListView, QCompleter, QStatusBar, QTableView, QTabWidget, QDockWidget, QFileDialog, QFormLayout, QGridLayout, QHBoxLayout,
#                              QHeaderView, QListWidget, QMainWindow, QMessageBox, QPushButton, QSizePolicy, QSpacerItem, QToolButton, QVBoxLayout, QWizardPage,
#                              QApplication, QButtonGroup, QRadioButton, QFontComboBox, QStackedWidget, QListWidgetItem, QSystemTrayIcon, QTreeWidgetItem,
#                              QDialogButtonBox, QAbstractItemView, QCommandLinkButton, QAbstractScrollArea, QGraphicsOpacityEffect, QTreeWidgetItemIterator)


# * Gid Imports ------------------------------------------------------------------------------------------------------------------------------------------------->

import gidlogger as glog

# from gidtools.gidfiles import (readit, clearit, readbin, writeit, loadjson, pickleit, writebin, pathmaker, writejson,
#                                dir_change, linereadit, get_pickled, ext_splitter, appendwriteit, create_folder, from_dict_to_file)


# * Local Imports ----------------------------------------------------------------------------------------------------------------------------------------------->
from gidvenv.utility.gidfiles_functions import pathmaker
from gidvenv.data.regex_data import package_value_regex
from gidvenv.req_handling.all_pip_packages import AllPackageNames
from gidvenv.utility.misc import check_if_filepath, check_if_url, cleaned_read_line
# endregion[Imports]

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


class RequirementItem:
    def __init__(self, package_name: str, version: str, specifier: str, options: list, extras: str) -> None:
        self.name = package_name
        self.version = version
        self.specifier = specifier
        self.options = options
        self.extras = extras

    @property
    def braced_extras(self):
        if self.extras:
            return f"[{self.extras}]"
        return None

    def __str__(self) -> str:
        _out = ' '.join(self.options) + f' {self.name}{self.braced_extras}{self.specifier}{self.version}'
        return _out.replace('None', '').strip()


class RequirementParser:
    package_regex = package_value_regex
    requirement_object = RequirementItem
    amount_options = 6

    def __init__(self) -> None:
        self.all_pip_names = AllPackageNames()

    def parse_file(self, file_path: str):
        for line in cleaned_read_line(file_path):
            if check_if_url(line) is True:
                yield self._parse_url(line)

            elif check_if_filepath(line) is True:
                yield self._parse_filepath(line)

            else:
                yield self._parse_regular_requirement(line)

    def _parse_regular_requirement(self, line: str):
        match = self.package_regex.match(line)
        if match:
            match_dict = match.groupdict()
            self._combine_options(match_dict)
            if match_dict.get('package_name') in self.all_pip_names:
                return self.requirement_object(**match_dict)
            else:
                raise RuntimeError(f'not a package "{match_dict.get("package_name")}"')

    def _parse_filepath(self, line: str):
        pass

    def _parse_url(self, line: str):
        pass

    def _combine_options(self, match_dict):
        _out = []
        for _num in range(1, self.amount_options + 1):
            option = match_dict.get(f"option{_num}")
            if option is not None:
                _out.append(option)
            del match_dict[f"option{_num}"]
        match_dict['options'] = _out


# region[Main_Exec]
if __name__ == '__main__':
    x = RequirementParser()
    for i in x.parse_file(r"D:\Dropbox\hobby\Modding\Programs\Github\My_Repos\Gid_Venv\tools\scratches\scratch_requirements.txt"):
        print(i)
# endregion[Main_Exec]
