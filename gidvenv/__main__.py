from gidvenv.venv_creation.venv_builder import GidEnvBuilder
from gidvenv.venv_settings.prepare_venv_settings import VenvSettingsHolder
import sys
import os
from icecream import ic
from gidvenv.utility.output_proxies import SpecialOutput
import click
from gidtools.gidfiles import pathmaker


@click.group()
def cli():
    pass


@cli.command()
@click.option('-vn', '--venv-folder-name', default=None)
@click.option('-m', '--main-dir', default='auto')
@click.option('-pp', '--pyproject-file', default=None)
@click.option('--verbose/-not-verbose', '-v/-nv', default=False)
@click.option('--manipulate-script/--dont-manipulate-script', '-m/-dm', default=True)
@click.option('-ei', '--extra-install-instructions', multiple=True)
def create(venv_folder_name, main_dir, pyproject_file, verbose, manipulate_script, extra_install_instructions):
    builder = GidEnvBuilder(main_dir=main_dir, pyproject_file=pyproject_file, verbose=verbose, manipulate_script=manipulate_script, extra_install_instructions=list(extra_install_instructions))
    venv_path = pathmaker(builder.main_dir, venv_folder_name) if venv_folder_name is not None else None
    builder.create(env_dir=venv_path)


@cli.command()
@click.option('-vd', '--venv-dir', default=None)
def initialize(venv_dir):
    builder = GidEnvBuilder()
    builder.initialize_only(env_dir=venv_dir)
    print('-- finished initializing venv setting infrastructure --')


@cli.command()
@click.argument('category')
@click.argument('value')
def add_default(category, value):
    if category not in VenvSettingsHolder.required_files_proto:
        category = category + '.txt'
    if category not in VenvSettingsHolder.required_files_proto:
        category = 'required_' + category
    VenvSettingsHolder.add_default(category, value)


@cli.command()
@click.argument('category')
@click.argument('value')
def remove_default(category, value):
    if category not in VenvSettingsHolder.required_files_proto:
        category = category + '.txt'
    if category not in VenvSettingsHolder.required_files_proto:
        category = 'required_' + category
    VenvSettingsHolder.remove_default(category, value)


def main():
    env_builder = GidEnvBuilder()
    env_builder.create()


if __name__ == '__main__':
    if len(sys.argv) == 1:
        raise RuntimeError("no input")
    cwd = sys.argv[1]
    if os.path.exists(cwd) is False:
        raise RuntimeError("input dir does not exist")
    if os.path.isdir(cwd) is False:
        cwd = os.path.dirname(cwd)
    os.chdir(cwd)

    main()
