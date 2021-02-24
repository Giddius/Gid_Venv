import os
import pytest
from gidvenv.utility.misc import cleaned_read_line, download_file
from tempfile import TemporaryDirectory


def test_cleaned_read_line(test_data_dir):
    x = cleaned_read_line(os.path.join(test_data_dir, 'cleaned_read_line_test_data.txt'))
    assert next(x) == "this is the first line"
    assert next(x) == "this is the second line"
    assert next(x) == "this is the third line after an empty line"
    with pytest.raises(StopIteration):
        next(x)
    x = cleaned_read_line(os.path.join(test_data_dir, 'cleaned_read_line_test_data.txt'))
    assert list(x) == ["this is the first line", "this is the second line", "this is the third line after an empty line"]


download_file_test_data = [()]


@pytest.mark.parametrize("url, extension, size", download_file_test_data)
def test_download_file():
    with TemporaryDirectory() as tempdir:
        out_path = os.path.join(tempdir, 'test_output_file')
