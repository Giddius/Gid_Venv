
# region [Imports]

# * Third Party Imports --------------------------------------------------------------------------------->
import requests
from validator_collection import validators
import validator_collection
import os
# endregion [Imports]


def download_file(url, output_file):
    """
    [summary]

    [extended_summary]

    Args:
        url ([type]): [description]
        output_file ([type]): [description]
    """
    response = requests.get(url, allow_redirects=True)
    response.raise_for_status()
    with open(output_file, 'wb') as out_file:
        out_file.write(response.content)


def cleaned_read_line(file_path: str):
    with open(file_path, 'r') as f:
        for line in f.readlines():
            line = line.strip()
            if line != '':
                yield line
