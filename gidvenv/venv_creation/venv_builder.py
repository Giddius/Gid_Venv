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
from contextlib import contextmanager, redirect_stdout, redirect_stderr
from statistics import mean, mode, stdev, median, variance, pvariance, harmonic_mean, median_grouped
from collections import Counter, ChainMap, deque, namedtuple, defaultdict
from urllib.parse import urlparse
from importlib.util import find_spec, module_from_spec, spec_from_file_location
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor
from importlib.machinery import SourceFileLoader
from venv import EnvBuilder
from typing import Optional
from pathlib import Path
from types import SimpleNamespace

# * Third Party Imports ----------------------------------------------------------------------------------------------------------------------------------------->


import toml
# import discord

# import requests

# import pyperclip

# import matplotlib.pyplot as plt

# from bs4 import BeautifulSoup

# from dotenv import load_dotenv

# from discord import Embed, File

# from discord.ext import commands, tasks

# from github import Github, GithubException


# from natsort import natsorted

# from fuzzywuzzy import fuzz, process
from icecream import ic

# * PyQt5 Imports ----------------------------------------------------------------------------------------------------------------------------------------------->

# from PyQt5.QtGui import QFont, QIcon, QBrush, QColor, QCursor, QPixmap, QStandardItem, QRegExpValidator

# from PyQt5.QtCore import (Qt, QRect, QSize, QObject, QRegExp, QThread, QMetaObject, QCoreApplication,
#                           QFileSystemWatcher, QPropertyAnimation, QAbstractTableModel, pyqtSlot, pyqtSignal)

# from PyQt5.QtWidgets import (QMenu, QFrame, QLabel, QAction, QDialog, QLayout, QWidget, QWizard, QMenuBar, QSpinBox, QCheckBox, QComboBox, QGroupBox, QLineEdit,
#                              QListView, QCompleter, QStatusBar, QTableView, QTabWidget, QDockWidget, QFileDialog, QFormLayout, QGridLayout, QHBoxLayout,
#                              QHeaderView, QListWidget, QMainWindow, QMessageBox, QPushButton, QSizePolicy, QSpacerItem, QToolButton, QVBoxLayout, QWizardPage,
#                              QApplication, QButtonGroup, QRadioButton, QFontComboBox, QStackedWidget, QListWidgetItem, QSystemTrayIcon, QTreeWidgetItem,
#                              QDialogButtonBox, QAbstractItemView, QCommandLinkButton, QAbstractScrollArea, QGraphicsOpacityEffect, QTreeWidgetItemIterator)

import colorama
from colorama import Fore, Back, Style
# * Gid Imports ------------------------------------------------------------------------------------------------------------------------------------------------->

import gidlogger as glog

from gidtools.gidfiles import (QuickFile, readit, clearit, readbin, writeit, loadjson, pickleit, writebin, pathmaker, writejson,
                               dir_change, linereadit, get_pickled, ext_splitter, appendwriteit, create_folder, from_dict_to_file)
from gidtools.gidfiles.file_system_walk import filesystem_walker, filesystem_walker_files, filesystem_walker_folders


# * Local Imports ----------------------------------------------------------------------------------------------------------------------------------------------->
from gidvenv.venv_settings.prepare_venv_settings import VenvSettingsHolder
from gidvenv.utility.script_data import LOAD_ENV_SNIPPET
from gidvenv.utility.misc import download_file
from gidvenv.utility.named_tuples import SetupCommandItem
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


class GidEnvBuilder(EnvBuilder):
    git_exe = shutil.which('git')

    base_venv_settings_defaults = {"system_site_packages": False,
                                   "clear": True,
                                   "symlinks": True,
                                   "with_pip": False,
                                   "prompt": None,
                                   "upgrade_deps": False}
    essentials = ['setuptools',
                  'wheel',
                  'PEP517',
                  'python-dotenv',
                  'flit']

    def __init__(self, main_dir: Union[str, Path] = 'auto', pyproject_file: Union[str, Path] = None, verbose: bool = False, manipulate_script: bool = True, extra_install_instructions: list = None, **kwargs) -> None:

        self.verbose = verbose
        self.manipulate_script = manipulate_script
        self.extra_install_instructions = extra_install_instructions
        self.main_dir = self._get_main_dir_from_git() if main_dir == 'auto' else pathmaker(main_dir)
        self.pyproject_file = self._find_pyproject_file(self.main_dir) if pyproject_file is None else pathmaker(pyproject_file)
        self.pyproject_data = toml.load(self.pyproject_file)

        self.project_name = self.pyproject_data["tool"]['flit']['metadata']['module']
        self.author_name = self.pyproject_data["tool"]['flit']['metadata']['author']
        os.environ['TARGET_PROJECT_NAME'] = self.project_name
        os.environ['TARGET_PROJECT_AUTHOR'] = self.author_name
        self.activation_script_file = None
        self.venv_dir = pathmaker(self.main_dir, '.venv')
        self.tools_dir = pathmaker(self.main_dir, 'tools')
        self.log_folder = pathmaker(self.tools_dir, 'create_venv_logs')
        self.error_log_file = pathmaker(self.log_folder, 'create_venv.errors')
        self.std_log_file = pathmaker(self.log_folder, 'create_venv.log')
        self.venv_setup_settings_dir = pathmaker(self.tools_dir, 'venv_setup_settings')

        self.venv_settings_holder = None
        self.dev_meta_env_file = None
        self.stdout = self._handle_stdout
        self.stderr = self._handle_stderr

        super().__init__(**self._handle_super_kwargs(**kwargs))

    @property
    def must_be_false_upgrade_setting(self):
        return False

    def _handle_super_kwargs(self, **kwargs):
        base_venv_data = self.pyproject_data['tool'].get('gidvenv', {}).get('base_venv_settings', self.base_venv_settings_defaults)
        for key, value in kwargs.items():
            if key in self.base_venv_settings_defaults:
                base_venv_data[key] = value
        base_venv_data['upgrade'] = self.must_be_false_upgrade_setting
        return base_venv_data

    @classmethod
    def with_pyproject_settings(cls, main_dir: Union[str, Path] = 'auto'):
        main_dir = cls._get_main_dir_from_git() if main_dir == 'auto' else pathmaker(main_dir)
        pyproject_file = cls._find_pyproject_file(main_dir)
        pyproject_data = toml.load(pyproject_file)
        return cls(main_dir=main_dir, pyproject_file=pyproject_file, ** pyproject_data['tool']['gidvenv']['settings'])

    def _handle_stdout(self, in_data):
        print(in_data)
        with open(self.std_log_file, 'a') as f:
            f.write(in_data + '\n')

    def _handle_stderr(self, in_data):
        if in_data != '':
            print(in_data)
            with open(self.error_log_file, 'a') as f:
                f.write(in_data + '\n')

    @classmethod
    def _get_main_dir_from_git(cls):
        cmd = subprocess.run([cls.git_exe, "rev-parse", "--show-toplevel"], capture_output=True, check=True, cwd=os.getcwd(), text=True)

        main_dir = pathmaker(cmd.stdout).rstrip('\n')
        if os.path.isdir(main_dir) is False:
            raise FileNotFoundError('Unable to locate main_dir')
        os.environ['WORKSPACE_FOLDER'] = main_dir
        return main_dir

    @staticmethod
    def _find_pyproject_file(main_dir):
        for file in filesystem_walker_files(main_dir):
            if file.name == 'pyproject.toml':
                return file.path
        raise FileNotFoundError('Unable to find "pyproject.toml" file')

    def run_script(self, script_item, in_venv=False):
        command = [script_item.executable] + script_item.args
        if in_venv is True:
            if self.activation_script_file is None:
                raise RuntimeError('activation script is None')
            command = [self.activation_script_file, '&&'] + command
        cmd = subprocess.run(command, check=False, capture_output=True, shell=True, text=True)
        self.stdout(cmd.stdout)
        self.stderr(cmd.stderr)
        if cmd.returncode != 0:
            if script_item.check is True:
                raise subprocess.CalledProcessError(cmd.returncode, cmd, cmd.stdout, cmd.stderr)
            self.stderr(f"--- ERROR with script '{script_item.executable}' ---")

    def _update_pip(self, context: SimpleNamespace) -> None:
        temp_folder = pathmaker(self.main_dir, 'temp')
        create_folder(temp_folder)
        get_pip_file = pathmaker(temp_folder, 'get-pip.py')
        download_file("https://bootstrap.pypa.io/get-pip.py", output_file=get_pip_file)
        if 'setuptools' in sys.modules:
            content = readit(get_pip_file)
            content = content.replace('import os.path', 'import setuptools\nimport os.path')
            writeit(get_pip_file, content)
        command_item = SetupCommandItem(context.env_exe, [get_pip_file], True, True)
        self.run_script(command_item)
        os.remove(get_pip_file)

    def _get_essentials(self, context: SimpleNamespace):
        for essential_name in self.essentials:
            script_item = SetupCommandItem('pip', ['install', essential_name, '--force-reinstall', '--no-cache-dir', '--upgrade'], True, False)
            self.run_script(script_item, in_venv=True)

    def _manipulate_activation_script(self, context: SimpleNamespace):
        bat_activation_file = pathmaker(context.bin_path, 'activate.bat')
        if self.manipulate_script is True:
            content = readit(bat_activation_file)
            content = content.replace('@echo off', LOAD_ENV_SNIPPET.replace('$!$DEV_META_ENV_FILE_PATH$!$', pathmaker(self.dev_meta_env_file, rev=True)))
            writeit(bat_activation_file, content)
        self.activation_script_file = bat_activation_file

    def _install_packages_from_settings(self, context: SimpleNamespace):
        install_order = [(self.venv_settings_holder.required_personal_packages, "required personal"),
                         (self.venv_settings_holder.required_misc, "required misc"),
                         (self.venv_settings_holder.required_experimental, "required experimental"),
                         (self.venv_settings_holder.required_qt, "required qt"),
                         (self.venv_settings_holder.required_from_github, "required from github"),
                         (self.venv_settings_holder.required_test, "required test"),
                         (self.venv_settings_holder.required_dev, "required dev")]
        for container in install_order:
            self.stdout(f'\n\n========================================== Installing {container[1].title()} Packages ==========================================\n')
            for item in container[0]:
                item.install(self.activation_script_file, self.stdout, self.stderr, self.extra_install_instructions, self.verbose)
            self.stdout(f"{'-'*100}")

    def _install_project_itself(self, context: SimpleNamespace):
        self.stdout("\n############ INSTALL THE PROJECT ITSELF AS -DEV PACKAGE ############\n")
        command = [self.activation_script_file, '&&', 'pushd', pathmaker(self.main_dir, rev=True), '&&', 'flit', 'install', '-s', '&', 'popd']
        cmd = subprocess.run(command, shell=True, capture_output=True, text=True, check=False)
        if cmd.returncode != 0:
            self.stderr(Back.RED + "--- ERROR with installing project itself ---")
        cmd_err = cmd.stderr
        cmd_out = cmd.stdout
        if 'error' in cmd_err.casefold():
            self.stderr(cmd_err)
        else:
            cmd_out += '\n' + cmd_err
        if self.verbose:
            self.stdout(cmd_out)

        if cmd.returncode == 0:
            self.stdout(f"{'-'*100}")
            self.stdout("- ################ " + Fore.WHITE + f"SUCCESSFULLY installed {Back.GREEN}{self.project_name} itself")

    def _create_dev_meta_env_file(self, context: SimpleNamespace):
        self.dev_meta_env_file = pathmaker(self.tools_dir, '_project_devmeta.env')
        with open(self.dev_meta_env_file, 'w') as dev_meta_f:
            dev_meta_f.write(f"WORKSPACEDIR={pathmaker(self.main_dir,rev=True)}\n")
            dev_meta_f.write(f"TOPLEVELMODULE={pathmaker(self.main_dir, self.project_name,rev=True)}\n")
            dev_meta_f.write(f"MAIN_SCRIPT_FILE={pathmaker(self.main_dir, self.project_name, '__main__.py',rev=True)}\n")
            dev_meta_f.write(f"PROJECT_NAME={self.project_name}\n")
            dev_meta_f.write(f"PROJECT_AUTHOR={self.author_name}\n")
            dev_meta_f.write(f"VENV_ACTIVATION_SCRIPT={pathmaker(context.bin_path, 'activate.bat')}")
            dev_meta_f.write("IS_DEV=true")

    def create(self, env_dir=None) -> None:
        env_dir = self.venv_dir if env_dir is None else env_dir
        create_folder(self.tools_dir)
        if os.path.isdir(self.venv_dir):
            shutil.rmtree(self.venv_dir)
        if os.path.isdir(self.log_folder):
            shutil.rmtree(self.log_folder)

        create_folder(self.log_folder)
        self.venv_settings_holder = VenvSettingsHolder(self.venv_setup_settings_dir)
        self.venv_settings_holder.collect()
        for script_item in self.venv_settings_holder.pre_setup_scripts:
            if script_item.enabled is True:
                self.run_script(script_item)

        return super().create(env_dir)

    def post_setup(self, context: SimpleNamespace) -> None:
        self.stdout('############## creating dev_meta_env_file')
        self._create_dev_meta_env_file(context)
        self.stdout('############## manipulate activation_script')
        self._manipulate_activation_script(context)
        self.stdout('############## updating pip')
        self._update_pip(context)
        self.stdout('############## getting essentials')
        self._get_essentials(context)
        self.stdout('############## installing packages')
        self._install_packages_from_settings(context)
        self.stdout('############## installing project')
        self._install_project_itself(context)

        # region[Main_Exec]
if __name__ == '__main__':
    pass
# endregion[Main_Exec]
