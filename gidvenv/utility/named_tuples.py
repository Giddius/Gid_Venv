from collections import namedtuple
import subprocess
from gidtools.gidfiles import pathmaker
from shutil import which


SetupCommandItem = namedtuple("ScriptItem", ['executable', 'args', 'enabled', 'check'], defaults=(True,))


def get_pip_exe():
    return which('pip')


def get_flit_exe():
    return which('flit')


class RequirementItem(namedtuple("RequirementItem", ['name', 'version_operator', 'version', 'install_instructions', 'extra_specifier', 'enabled'])):

    def install(self, activation_script, stdout, stderr, extra_install_instructions: list = None, verbose=False):
        if self.enabled:
            install_instructions = self.install_instructions
            if extra_install_instructions is not None:
                for extra_instruction in extra_install_instructions:
                    if extra_instruction not in install_instructions:
                        install_instructions.append(extra_instruction)
            if verbose:
                stdout(f"#### Installing {self.name.upper()} ####\n")
            command = [activation_script, '&&', "pip", "install"] + install_instructions + [f"{self.name}{self.version_operator}{self.version}"]
            cmd = subprocess.run(command, capture_output=True, check=False, shell=True, text=True)
            if cmd.returncode != 0 or cmd.stderr != '':
                stderr(f"--- ERROR with installing pypi package {self.name.upper()} ---")
            if verbose:
                stdout(cmd.stdout)
            stderr(cmd.stderr)

            if cmd.returncode == 0:
                stdout(f"{'-'*100}")
                stdout("- ################ " + f"SUCCESSFULLY installed {self.name.upper()} ")


class PersonalRequiredItem(namedtuple("PersonalRequiredItem", ['name', 'path', 'enabled'])):

    def install(self, activation_script, stdout, stderr, extra_install_instructions: list = None, verbose=False):
        if self.enabled:
            path = pathmaker(self.path, rev=True)
            if verbose:
                stdout(f"#### Installing flit dev {self.name.upper()} from {path} ####\n")
            command = [activation_script, '&&', 'pushd', path, '&&', "flit", 'install', '-s', '&', "popd"]
            cmd = subprocess.run(command, capture_output=True, check=False, shell=True, text=True)
            if cmd.returncode != 0:
                stderr(f"--- ERROR with installing flit dev package {self.name.upper()} ---")
            cmd_out = cmd.stdout

            cmd_err = cmd.stderr
            if 'error' in cmd_err.casefold():
                stderr(cmd_err)
            else:
                cmd_out += '\n' + cmd_err

            if verbose:
                stdout(cmd_out)

            if cmd.returncode == 0:
                stdout(f"{'-'*100}")
                stdout("- ################ " + f"SUCCESSFULLY installed {self.name.upper()} ")


class GithubRequiredItem(namedtuple("GithubRequiredItem", ['name', 'url', 'enabled'])):

    def install(self, activation_script, stdout, stderr, extra_install_instructions: list = None, verbose=False):
        if self.enabled:
            if verbose:
                stdout(f"#### Installing from Github {self.name.upper()} ####\n")
            url = self.url
            if not url.startswith('git+'):
                url = 'git+' + url
            install_instructions = extra_install_instructions if extra_install_instructions is not None else []
            command = [activation_script, '&&', "pip", "install", '--no-cache-dir'] + install_instructions + [url]
            cmd = subprocess.run(command, capture_output=True, check=False, shell=True, text=True)
            if cmd.returncode != 0:
                stderr(f"--- ERROR with installing Github package {self.name.upper()} ---")
            cmd_out = cmd.stdout

            cmd_err = cmd.stderr
            if 'error' in cmd_err.casefold():
                stderr(cmd_err)
            else:
                cmd_out += '\n' + cmd_err

            if verbose:
                stdout(cmd.stdout)

            if cmd.returncode == 0:
                stdout(f"{'-'*100}")
                stdout("- ################ " + f"SUCCESSFULLY installed {self.name.upper()} ")
