import os

os.environ["IS_TEST"] = "1"

import pytest
from gidvenv.utility.subprocessor import Subprocessor
from gidvenv.utility.gidfiles_functions import pathmaker


def stdout_printer(in_text):
    print(f"+STDOUT+ {in_text}")


def stderr_printer(in_text):
    print(f"-STDERR- {in_text}")


def test_main_dir_from_git():
    processor = Subprocessor(stdout_printer, stderr_printer, True)
    assert processor.main_dir_from_git().endswith('/Gid_Venv')


def test_call(capfd):
    processor = Subprocessor(stdout_printer, stderr_printer, True)
    processor(['Python', '-V'])
    out, err = capfd.readouterr()
    assert out.strip('\n') == "+STDOUT+ Python 3.9.1"
