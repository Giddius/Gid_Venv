import pytest
import os
import sys
import shutil
from tempfile import TemporaryDirectory
from gidtools.gidfiles import writeit, readit, pathmaker
from textwrap import dedent

FAKE_PYPROJECT = dedent("""[tool.flit.metadata]
                module = "fakeproject"
                author = "brocaprogs"
                home-page = "https://github.com/Giddius/fakeproject"
                classifiers = ["License :: OSI Approved :: MIT License"]
                description-file = "README.md"
                license = "MIT"
                requires = []
                """)


@pytest.fixture
def fresh_package_dir(tmpdir):
    folder = pathmaker(str(tmpdir), 'fake_project')
    os.makedirs(folder)
    writeit(pathmaker(folder, 'pyproject.toml'), FAKE_PYPROJECT)
    user_data_storage_dir = pathmaker(str(tmpdir), 'user_data_storage')
    os.environ['USER_DATA_STORAGE_DIR'] = user_data_storage_dir
    os.chdir(folder)
    yield pathmaker(folder)
    venv_folder = pathmaker(folder, '.venv')
    for dirname, folderlist, filelist in os.walk(venv_folder):
        for file in filelist:
            path = pathmaker(dirname, file)
            if os.path.islink(path) is True:
                os.unlink(path)

        for folder in folderlist:
            folder_path = pathmaker(dirname, folder)
            if os.path.islink(folder_path):
                os.rmdir(folder_path)
