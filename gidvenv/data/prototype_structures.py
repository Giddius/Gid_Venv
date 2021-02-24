REQUIRED_FILES_PROTO = {"post_setup_scripts.txt": [],
                        "pre_setup_scripts.txt": [],
                        "required_dev.txt": [],
                        "required_from_github.txt": [],
                        "required_misc.txt": [],
                        "required_personal_packages.txt": [],
                        "required_qt.txt": [],
                        "required_test.txt": ["pytest"],
                        "required_experimental.txt": []}

ESSENTIALS_DEFAULTS = ['setuptools',
                       'wheel',
                       'PEP517',
                       'flit']

TOOL_DIR_NAME = "tools"

SETTINGS_DIR_NAME = "venv_setup_settings"

DEFAULTS_PROTO_CONTENT = {"required": REQUIRED_FILES_PROTO,
                          "essentials": ESSENTIALS_DEFAULTS,
                          "tool_folder_name": TOOL_DIR_NAME,
                          "settings_folder_name": SETTINGS_DIR_NAME}
