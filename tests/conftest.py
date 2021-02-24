import os
import pytest
THIS_FILE_DIR = os.path.abspath(os.path.dirname(__file__))


@pytest.fixture()
def test_data_dir():
    return os.path.join(THIS_FILE_DIR, 'test_data')
