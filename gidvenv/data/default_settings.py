
GIDVENV_SETTINGS_DEFAULTS = {'verbose': False,
                             'manipulate_script': True,
                             'extra_install_instructions': [],
                             "pyclean_before": True}

BASE_VENV_SETTINGS_DEFAULTS = {"system_site_packages": False,
                               "clear": True,
                               "symlinks": True,
                               "with_pip": False,
                               "prompt": None,
                               "upgrade_deps": False}


PYPROJECT_GIDVENV_TOOL_SECTION = 'gidvenv'

GIDVENV_PYPROJECT_SUBSECTIONS = {'base_venv_settings': BASE_VENV_SETTINGS_DEFAULTS,
                                 'settings': GIDVENV_SETTINGS_DEFAULTS}
