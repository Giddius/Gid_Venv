from gidvenv.venv_settings.prepare_venv_settings import VenvSettingsHolder
from gidvenv.utility.named_tuples import SetupCommandItem, RequirementItem, GithubRequiredItem, PersonalRequiredItem
import sys
import os
import shutil
from icecream import ic
from gidtools.gidfiles import pathmaker


def test_file_creation(empty_venv_settings_folder):

    assert {file for file in os.listdir(empty_venv_settings_folder)} == set()
    settings_holder = VenvSettingsHolder(empty_venv_settings_folder)
    settings_holder._ensure_settings_file_exist()
    assert set(os.listdir(empty_venv_settings_folder)) == set([key for key in settings_holder.required_files])
    for file in os.scandir(empty_venv_settings_folder):
        if file.is_file():
            with open(file.path, 'r') as f:
                content = f.read()
            assert content == '\n'.join(settings_holder.required_files.get(file.name))


def test_parse_requirements(empty_venv_settings_folder):
    temp_user_dir = pathmaker(empty_venv_settings_folder, 'temp_user_dir')
    os.makedirs(temp_user_dir)
    os.environ['USER_DATA_STORAGE_DIR'] = pathmaker(temp_user_dir)
    VenvSettingsHolder.user_data_dir = temp_user_dir
    settings_holder = VenvSettingsHolder(empty_venv_settings_folder)
    settings_holder.collect()

    assert settings_holder.pre_setup_scripts == [SetupCommandItem(shutil.which("pskill64"), ["Dropbox", "-t", "-nobanner"], False, False)]
    assert RequirementItem("icecream", "", "", [], "", True) in settings_holder.required_dev
    assert RequirementItem("numpy", "==", "1.19.3", ["--force-reinstall"], "", True) in settings_holder.required_dev

    assert GithubRequiredItem(url="https://github.com/pyinstaller/pyinstaller.git", name="pyinstaller", enabled=True) in settings_holder.required_from_github

    assert PersonalRequiredItem(name="gidconfig", path=r"D:/Dropbox/hobby/Modding/Programs/Github/My_Repos/GidConfig", enabled=True) in settings_holder.required_personal_packages


def test_write_back(empty_venv_settings_folder):
    settings_holder = VenvSettingsHolder(empty_venv_settings_folder)
    settings_holder.collect()
    for file in os.scandir(empty_venv_settings_folder):
        if file.is_file():
            with open(file.path, 'r') as f:
                content = f.read()
            assert {line for line in content.splitlines() if line != ''} == {line for line in '\n'.join(settings_holder.required_files.get(file.name)).splitlines() if line != ''}
