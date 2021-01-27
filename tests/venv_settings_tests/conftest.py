import pytest
from tempfile import TemporaryDirectory
from gidvenv.utility.gidfiles_functions import pathmaker
import os


@pytest.fixture
def empty_venv_settings_folder(tmpdir):

    tool_folder = pathmaker(str(tmpdir), 'tools')
    os.makedirs(tool_folder)
    venv_settings_folder = pathmaker(tool_folder, 'venv_setup_settings')
    os.makedirs(venv_settings_folder)

    return venv_settings_folder
