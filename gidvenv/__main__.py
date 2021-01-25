from gidvenv.venv_creation.venv_builder import GidEnvBuilder
import sys
import os
from icecream import ic
from gidvenv.utility.output_proxies import SpecialOutput


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
