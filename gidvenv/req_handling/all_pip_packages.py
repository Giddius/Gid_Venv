"""
[summary]

[extended_summary]
"""

# region [Imports]

# * Standard Library Imports ---------------------------------------------------------------------------->
import os
from datetime import datetime, timedelta
# * Third Party Imports --------------------------------------------------------------------------------->
import requests
from lxml import html
import json
from fuzzywuzzy import fuzz, process as fuzzprocess
# * Gid Imports ----------------------------------------------------------------------------------------->
import gidlogger as glog

# * Local Imports --------------------------------------------------------------------------------------->
from gidvenv.utility.gidfiles_functions import loadjson, pathmaker, writejson, create_folder, pickleit, get_pickled
from gidvenv import appdata_dir
from gidvenv.data.misc_data import SIMPLE_PYPI_URL
# endregion [Imports]


# region [TODO]


# endregion [TODO]

# region [AppUserData]


# endregion [AppUserData]

# region [Logging]

log = glog.aux_logger(__name__)

# endregion[Logging]

# region [Constants]

THIS_FILE_DIR = os.path.abspath(os.path.dirname(__file__))

# endregion[Constants]


class AllPackageNames():
    save_file_name = 'all_pypi_package_names.json'
    last_updated_file = f'last_updated_{os.path.splitext(save_file_name)[0]}.pkl'
    update_interval = timedelta(days=1)

    def __init__(self):
        self.package_names = None
        self.package_names_as_list = None

        self.load_data()

    @property
    def cleaned_up_package_names(self):
        for name in self.package_names_as_list:
            if name != '' and len(name) > 2:
                yield name

    @classmethod
    def refresh_pypi_names(cls):
        response = requests.get(SIMPLE_PYPI_URL)
        if response.status_code == 404:
            # TODO: Custom ERROR
            raise RuntimeError("unable to refresh package name list")
        package_names = map(lambda x: x.casefold(), html.fromstring(response.content).xpath('//a/text()'))
        cls.save_data(package_names)

    @classmethod
    def save_data(cls, data):
        create_folder(appdata_dir)
        data = sorted(data)
        current_datetime = datetime.now()
        writejson(data, pathmaker(appdata_dir, cls.save_file_name))
        pickleit(current_datetime, pathmaker(appdata_dir, cls.last_updated_file))

    def _check_last_updated(self):
        last_updated_path = pathmaker(appdata_dir, self.last_updated_file)
        if os.path.isfile(last_updated_path) is False or os.path.isfile(pathmaker(appdata_dir, self.save_file_name)) is False or get_pickled(last_updated_path) + self.update_interval <= datetime.now():

            self.refresh_pypi_names()

    def load_data(self):
        self._check_last_updated()
        data_path = pathmaker(appdata_dir, self.save_file_name)
        self.package_names_as_list = loadjson(data_path)
        self.package_names = set(self.package_names_as_list)

    def get_name_correction(self, errored_name):
        _out = fuzzprocess.extractOne(query=errored_name, choices=self.package_names, processor=fuzz.ratio, score_cutoff=60)
        if _out is None:
            return ''
        return f"Did you maybe mean: '{_out[0]}' ?"

    def __call__(self, as_set=True):
        return self.package_names if as_set is True else self.package_names_as_list

    def __str__(self):
        return self.__class__.__name__

    def __contains__(self, other):
        return other.casefold() in self.package_names


# region[Main_Exec]
if __name__ == '__main__':
    pass
# endregion[Main_Exec]
