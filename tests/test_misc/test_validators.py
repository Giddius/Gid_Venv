import os
os.environ['IS_TEST'] = '1'

from gidvenv.utility.validators import check_if_url, check_if_filepath
import pytest


possible_urls_test_data = [("https://github.com/overfl0/Armaclass.git", (True, False)),
                           ("https://github.com/pyinstaller/pyinstaller/tarball/develop", (True, False)),
                           ("validator-collection", (False, False)),
                           ("paramiko[all]", (False, False)),
                           ("D:\Dropbox\hobby\Modding\Programs\Github\My_Repos\GidConfig,gidconfig", (False, True)),
                           ("D:\Dropbox\hobby\Modding\Programs\Github\My_Repos\GidConfig", (False, True)),
                           ("PyQt5", (False, False)),
                           ("parceqt", (False, False)),
                           ("PyQt5-stubs", (False, False)),
                           ("pyqt5-tools", (False, False)),
                           ("pyqt5-plugins", (False, False)),
                           ("qt5-applications", (False, False)),
                           ("pyqtgraph", (False, False)),
                           ("pyopengl", (False, False)),
                           ("QScintilla", (False, False)),
                           ("PyQtWebEngine", (False, False)),
                           ("PyQtDataVisualization", (False, False)),
                           ("PyQtChart", (False, False)),
                           ("PyQt3D", (False, False)),
                           ("create_venv_extra_envvars.py,%WORKSPACE_FOLDER% %PROJECT_NAME% %PROJECT_AUTHOR%", (False, False)),
                           ]


@pytest.mark.parametrize("line_input, expected", possible_urls_test_data)
def test_check_if_url(line_input, expected):
    assert check_if_url(line_input) is expected[0]


@pytest.mark.parametrize("line_input, expected", possible_urls_test_data)
def test_check_if_filepath(line_input, expected):
    assert check_if_filepath(line_input) is expected[1]
