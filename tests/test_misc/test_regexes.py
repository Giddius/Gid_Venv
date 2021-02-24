import os
os.environ['IS_TEST'] = '1'


from gidvenv.data.regex_data import package_value_regex
import pytest


def is_not_None(in_object):
    return in_object is not None


def is_None(in_object):
    return in_object is None


package_value_test_data = [("memory-profiler", {"match_state": is_not_None, "package_name": "memory-profiler"}),
                           ("--force-reinstall numpy", {"match_state": is_not_None, "option1": "--force-reinstall", "package_name": "numpy"}),
                           ("--force-reinstall numpy==1.19.3", {"match_state": is_not_None, "option1": "--force-reinstall", "package_name": "numpy", "specifier": "==", "version": "1.19.3"}),
                           ("paramiko[all]", {"match_state": is_not_None, "package_name": "paramiko", 'extras': 'all'}),
                           ("This//will//:Fail", {"match_state": is_None}),
                           ("PyQt5", {"match_state": is_not_None, "package_name": "PyQt5"}),
                           ("parceqt", {"match_state": is_not_None, "package_name": "parceqt"}),
                           ("PyQt5-stubs", {"match_state": is_not_None, "package_name": "PyQt5-stubs"}),
                           ("pyqt5-tools", {"match_state": is_not_None, "package_name": "pyqt5-tools"}),
                           ("pyqt5-plugins", {"match_state": is_not_None, "package_name": "pyqt5-plugins"}),
                           ("qt5-applications", {"match_state": is_not_None, "package_name": "qt5-applications"}),
                           ("pyqtgraph", {"match_state": is_not_None, "package_name": "pyqtgraph"}),
                           ("pyopengl", {"match_state": is_not_None, "package_name": "pyopengl"}),
                           ("QScintilla", {"match_state": is_not_None, "package_name": "QScintilla"}),
                           ("PyQtWebEngine", {"match_state": is_not_None, "package_name": "PyQtWebEngine"}),
                           ("PyQtDataVisualization", {"match_state": is_not_None, "package_name": "PyQtDataVisualization"}),
                           ("PyQtChart", {"match_state": is_not_None, "package_name": "PyQtChart"}),
                           ("PyQt3D", {"match_state": is_not_None, "package_name": "PyQt3D"}),
                           ("PyQt5_sip==12.8.1", {"match_state": is_not_None, "package_name": "PyQt5_sip", "specifier": "==", "version": "12.8.1"}),
                           ("pyfiglet==0.8.post1", {"match_state": is_not_None, "package_name": "pyfiglet", 'specifier': '==', 'version': '0.8.post1'})]


@pytest.mark.parametrize("line_input, expected", package_value_test_data)
def test_package_value_regex(line_input, expected):
    match = package_value_regex.match(line_input)

    assert expected.get('match_state', is_not_None)(match) is True
    if match:

        for i in range(1, 7):
            option = f"option{i}"
            assert match.group(option) == expected.get(option, None)
        assert match.group("package_name") == expected.get('package_name', None)
        assert match.group('extras') == expected.get('extras', None)
        assert match.group('specifier') == expected.get('specifier', None)
        assert match.group('version') == expected.get('version', None)
