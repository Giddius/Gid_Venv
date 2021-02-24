
# region [Imports]

# * Third Party Imports --------------------------------------------------------------------------------->
import requests
from validator_collection import validators
import validator_collection
import os
# endregion [Imports]


def check_if_url(possible_url: str):
    """
    checks if input `possible_url` is and valid url.

    Appends "https://" in front of it beforehand. (maybe not necessary).

    Args:
        possible_url `str`: The string to check.

    Returns:
        `bool`: `True` if it is and valid url.
    """
    if not possible_url.startswith('http://') and not possible_url.startswith('https://'):
        possible_url = 'https://' + possible_url
    try:
        validators.url(possible_url)
        return True
    except validator_collection.errors.InvalidURLError:
        return False


def check_if_filepath(possible_file_path):
    if ',' in possible_file_path:
        possible_file_path = possible_file_path.split(',')[0]
    return os.path.exists(possible_file_path)
