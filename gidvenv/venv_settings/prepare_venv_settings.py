
# * Standard Library Imports ---------------------------------------------------------------------------->
import os
import sys
import shutil
from pathlib import Path
from gidtools.gidfiles import pathmaker, writeit, readit, create_folder, loadjson, writejson
from gidvenv.utility.named_tuples import RequirementItem, GithubRequiredItem, PersonalRequiredItem, SetupCommandItem
from gidvenv.venv_settings.all_pip_packages import AllPackageNames
from pprint import pprint


class VenvSettingsHolder:

    user_data_dir = os.getenv("USER_DATA_STORAGE_DIR")
    defaults_file_name = 'defaults.json'
    required_files_proto = {"post_setup_scripts.txt": [],
                            "pre_setup_scripts.txt": ["# pskill64,Dropbox -t -nobanner"],
                            "required_dev.txt": ["icecream", "--force-reinstall numpy==1.19.3", "isort", "memory-profiler", "matplotlib", "pydeps", "pipreqs", "invoke"],
                            "required_from_github.txt": ["https://github.com/pyinstaller/pyinstaller.git"],
                            "required_misc.txt": ["python-benedict", "fuzzywuzzy", "python-Levenshtein", "click"],
                            "required_personal_packages.txt": [r"D:\Dropbox\hobby\Modding\Programs\Github\My_Repos\Gid_Vscode_Wrapper,gid_vscode_wrapper",
                                                               r"D:\Dropbox\hobby\Modding\Programs\Github\My_Repos\gidtools_utils,gidtools",
                                                               r"D:\Dropbox\hobby\Modding\Programs\Github\My_Repos\GidConfig,gidconfig",
                                                               r"D:\Dropbox\hobby\Modding\Programs\Github\My_Repos\GidAppData,gidappdata",
                                                               r"D:\Dropbox\hobby\Modding\Programs\Github\My_Repos\gidlogger_rep,gidlogger",
                                                               r"D:\Dropbox\hobby\Modding\Programs\Github\My_Repos\Gid_View_models,gidviewmodels"],
                            "required_qt.txt": [],
                            "required_test.txt": ["pytest", "pytest-venv", "pytest-cov", "pytest-click"],
                            "required_experimental.txt": []}

    def __init__(self, settings_dir) -> None:
        self.defaults_file = pathmaker(self.user_data_dir, 'defaults.json')
        if os.path.isfile(self.defaults_file) is False:
            writejson(self.required_files_proto, self.defaults_file)
        self.required_files = loadjson(self.defaults_file)
        self.folder = pathmaker(settings_dir)
        create_folder(self.folder)
        self.all_packages = AllPackageNames()
        self.pre_setup_scripts = []
        self.post_setup_scripts = []
        self.required_misc = []
        self.required_qt = []
        self.required_test = []
        self.required_experimental = []
        self.required_dev = []
        self.required_personal_packages = []
        self.required_from_github = []
        self.requirements_parse_table = {"required_dev": {"parsing": self._standard_req_parse, "writing": self._standard_req_write},
                                         "required_from_github": {"parsing": self._github_url_req_parse, "writing": self._github_url_req_write},
                                         "required_misc": {"parsing": self._standard_req_parse, "writing": self._standard_req_write},
                                         "required_personal_packages": {"parsing": self._personal_flit_req_parse, "writing": self._personal_flit_req_write},
                                         "required_qt": {"parsing": self._standard_req_parse, "writing": self._standard_req_write},
                                         "required_test": {"parsing": self._standard_req_parse, "writing": self._standard_req_write},
                                         "required_experimental": {"parsing": self._standard_req_parse, "writing": self._standard_req_write}}

    @classmethod
    def add_default(cls, category, value):
        path = pathmaker(cls.user_data_dir, cls.defaults_file_name)
        if os.path.isfile(path) is False:
            writejson(cls.required_files_proto, path)
        data = loadjson(path)
        if category not in data:
            print('no such default category')
            return
        data[category].append(value)
        print(f"added value '{value}' to category '{category}'")
        writejson(data, path)

    @classmethod
    def remove_default(cls, category, value):
        path = pathmaker(cls.user_data_dir, cls.defaults_file_name)
        if os.path.isfile(path) is False:
            writejson(cls.required_files_proto, path)
        data = loadjson(path)
        if category not in data:
            print('no such default category')
            return
        to_remove_index = None
        for index, item in enumerate(data[category]):
            if value.casefold() in item.casefold():
                to_remove_index = index
                break
        if to_remove_index is None:
            print("no such value found")
            return
        removed_value = data[category].pop(to_remove_index)
        print(f"removed value '{removed_value}' from category '{category}'")
        writejson(data, path)

    def _ensure_settings_file_exist(self):
        for required_file, default_content in self.required_files.items():
            path = pathmaker(self.folder, required_file)
            if os.path.isfile(path) is False:
                writeit(path, '\n'.join(default_content))

    def _validate_executable(self, executable):
        executable = executable.strip('"')
        if os.path.isfile(executable):
            return executable
        _executable = shutil.which(executable)
        if _executable is None:
            raise FileNotFoundError(f"Unable to locate '{executable}'")
        return _executable

    def _split_convert_args(self, args_data):
        args = args_data.split(' ')
        args = list(map(os.path.expandvars, args))
        return args

    def parse_setup_commands(self):
        for setup_command_file in [key for key in self.required_files if 'setup_scripts' in key]:
            category = os.path.splitext(setup_command_file)[0]
            path = pathmaker(self.folder, setup_command_file)
            for line in readit(path).splitlines():
                line = line.strip()
                if line != '':
                    enabled = True
                    check = False
                    if line.startswith('#'):

                        line = line.removeprefix('#').strip()
                        enabled = False
                    if line.startswith('--check'):
                        line = line.removeprefix('--check').strip()
                        check = True
                    executable, args = line.split(',')
                    getattr(self, category).append(SetupCommandItem(executable=self._validate_executable(executable), args=self._split_convert_args(args), enabled=enabled, check=check))

    def _standard_req_parse(self, line, enabled):
        install_instructions = []
        for token in line.split(' '):
            if token.startswith('--'):
                install_instructions.append(token)
                line = line.replace(token, '')
        line = line.strip()
        version_operator = ''
        version = ''
        package_name = line
        possible_operators = ['==', '>=', '<=', '>', '<']
        for possible_operator in possible_operators:
            if possible_operator in line:
                version_operator = possible_operator
                package_name, version = line.split(possible_operator)
                break
        extra_specifier = ''
        if '[' in package_name:
            package_name, extra_specifier = package_name.split('[')
            extra_specifier = extra_specifier.strip(']')
        if package_name not in self.all_packages and package_name.replace('_', '-') not in self.all_packages:
            raise KeyError(f'package "{package_name}" is not a valid pypi package')
        return RequirementItem(name=package_name, version_operator=version_operator, version=version, install_instructions=install_instructions, extra_specifier=extra_specifier, enabled=enabled)

    def _personal_flit_req_parse(self, line, enabled):
        package_path, package_name = line.split(',')
        if os.path.isdir(package_path) is False:
            raise FileNotFoundError(f"{package_path=} does not exist")
        return PersonalRequiredItem(name=package_name, path=pathmaker(package_path), enabled=enabled)

    def _github_url_req_parse(self, line, enabled):
        package_name = line.split('/')[-1].split('.')[0]
        return GithubRequiredItem(name=package_name, url=line, enabled=enabled)

    def parse_requirements(self):
        for req_file in [key for key in self.required_files if 'setup_scripts' not in key]:
            category = os.path.splitext(req_file)[0]
            path = pathmaker(self.folder, req_file)
            func = self.requirements_parse_table.get(category).get('parsing')
            container = getattr(self, category)
            lines = readit(path).splitlines()
            # lines = sorted(lines, key=len, reverse=True)
            for line in lines:

                line = line.strip()
                if line != '':
                    enabled = True
                    if line.startswith('#'):
                        enabled = False
                        line = line.removeprefix('#').strip()
                    package_item = func(line, enabled)
                    if package_item.name not in [item.name for item in container]:
                        container.append(package_item)
            # setattr(self, category, sorted(getattr(self, category), key=lambda x: (len(getattr(x, 'version', '')), x.name), reverse=True))
            # setattr(self, category, sorted(getattr(self, category), key=lambda x: len(getattr(x, 'install_instructions', '')), reverse=True))

    def _standard_req_write(self, items):
        _out = []
        for item in items:
            prefix = '# ' if item.enabled is False else ''
            extra_specifier = f"[{item.extra_specifier}]" if item.extra_specifier != '' else ''
            install_instructions = ' '.join(item.install_instructions) + ' ' if item.install_instructions != [] else ''
            _out.append(f"{prefix}{install_instructions}{item.name}{extra_specifier}{item.version_operator}{item.version}".strip())
        return _out

    def _personal_flit_req_write(self, items):
        _out = []
        for item in items:
            prefix = '# ' if item.enabled is False else ''
            _out.append(f"{prefix}{pathmaker(item.path, rev=True)},{item.name}".strip())
        return _out

    def _github_url_req_write(self, items):
        _out = []
        for item in items:
            prefix = '# ' if item.enabled is False else ''
            _out.append(f"{prefix}{item.url}".strip())
        return _out

    def write_cleaned_settings_file(self):
        for req_file in [key for key in self.required_files if 'setup_scripts' not in key]:
            category = os.path.splitext(req_file)[0]
            path = pathmaker(self.folder, req_file)
            func = self.requirements_parse_table.get(category).get('writing')
            items = getattr(self, category)
            # items = sorted(getattr(self, category), key=lambda x: (len(getattr(x, 'version', '')), x.name), reverse=True)
            # items = sorted(items, key=lambda x: len(getattr(x, 'install_instructions', '')), reverse=True)
            with open(path, 'w') as f:
                f.write('\n'.join(func(items)))

    def collect(self, write_cleaned=True):
        self._ensure_settings_file_exist()
        self.parse_setup_commands()
        self.parse_requirements()
        if write_cleaned is True:
            self.write_cleaned_settings_file()


if __name__ == '__main__':
    pass
