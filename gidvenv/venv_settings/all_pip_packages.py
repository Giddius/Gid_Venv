"""
[summary]

[extended_summary]
"""

# region [Imports]

# * Standard Library Imports ---------------------------------------------------------------------------->
import os

# * Third Party Imports --------------------------------------------------------------------------------->
import requests
from lxml import html

# * Gid Imports ----------------------------------------------------------------------------------------->
import gidlogger as glog

# * Local Imports --------------------------------------------------------------------------------------->
from gidvenv.utility.gidfiles_functions import loadjson, pathmaker, writejson, create_folder

# endregion [Imports]


# region [TODO]


# endregion [TODO]

# region [AppUserData]


# endregion [AppUserData]

# region [Logging]

log = glog.aux_logger(os.getenv('APP_NAME'))

# endregion[Logging]

# region [Constants]

THIS_FILE_DIR = os.path.abspath(os.path.dirname(__file__))

# endregion[Constants]


class AllPackageNames():
    save_file_name = 'all_pypi_package_names.json'

    def __init__(self):
        self.simple_pypi_url = "https://pypi.org/simple/"
        self.package_names = None

    def get_pypi_names(self):
        response = requests.get(self.simple_pypi_url)
        if response.status_code != 404:
            self.package_names = set(map(lambda x: x.casefold(), html.fromstring(
                response.content).xpath('//a/text()')))
        else:
            self.package_names = self.load_data()
        self.save_data()

    def save_data(self):
        create_folder(os.getenv("USER_DATA_STORAGE_DIR"))
        path = pathmaker(os.getenv("USER_DATA_STORAGE_DIR"),
                         self.save_file_name)
        data = list(self.package_names)
        data = sorted(data)
        writejson(data, path)

    def load_data(self):
        path = pathmaker(os.getenv("USER_DATA_STORAGE_DIR"),
                         self.save_file_name)
        if os.path.isfile(path) is False:
            raise RuntimeError(
                'cannot retrieve package names, and not old data saved')
        data = loadjson(path)
        return set(data)

    def __str__(self):
        return self.__class__.__name__

    def __contains__(self, other):
        if self.package_names is None:
            self.get_pypi_names()
        return other.casefold() in self.package_names


# region[Main_Exec]
if __name__ == '__main__':
    pass
# endregion[Main_Exec]
