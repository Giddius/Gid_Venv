from gidvenv.venv_creation.venv_builder import GidEnvBuilder
from gidtools.gidfiles import pathmaker
import os
import subprocess


def test_pyproject_reading(fresh_package_dir):
    builder = GidEnvBuilder(main_dir=fresh_package_dir)
    assert builder.main_dir == fresh_package_dir
    assert builder.pyproject_file == pathmaker(fresh_package_dir, 'pyproject.toml')
    assert builder.project_name == 'fakeproject'
    assert builder.author_name == 'brocaprogs'

    assert builder.venv_dir == pathmaker(fresh_package_dir, '.venv')
    assert builder.tools_dir == pathmaker(fresh_package_dir, 'tools')
    assert builder.log_folder == pathmaker(fresh_package_dir, 'tools', 'create_venv_logs')
    assert builder.venv_setup_settings_dir == pathmaker(fresh_package_dir, 'tools', 'venv_setup_settings')

    assert os.getenv('TARGET_PROJECT_NAME') == "fakeproject"
    assert os.getenv("TARGET_PROJECT_AUTHOR") == "brocaprogs"


def test_venv_creation(fresh_package_dir):
    assert {item.name for item in os.scandir(fresh_package_dir)} == {'pyproject.toml'}
    builder = GidEnvBuilder(main_dir=fresh_package_dir)
    assert builder.main_dir == fresh_package_dir
    assert {item.name for item in os.scandir(fresh_package_dir)} == {'pyproject.toml'}
    builder.create()
    assert {item.name for item in os.scandir(fresh_package_dir)} == {'pyproject.toml', '.venv', 'temp', 'tools'}
    cmd = subprocess.run([builder.activation_script_file, '&&', 'pip', 'freeze'], check=True, capture_output=True, text=True)
    installed_packs = []
    for line in cmd.stdout.splitlines():
        if line != '' and '@' not in line:
            name = line.split('==')[0].strip()
            installed_packs.append(name.casefold())
    installed_packs = set(installed_packs)
    should_installed_packs = []
    for key, value in builder.venv_settings_holder.required_files.items():
        if all(excl_string not in key for excl_string in ['post_setup', 'pre_setup', 'from_github', 'personal_packages']):
            for packa in value:
                name = packa.split(' ')[-1].split('==')[0].strip()
                should_installed_packs.append(name.casefold())
    assert all(should_pack in installed_packs for should_pack in should_installed_packs)
