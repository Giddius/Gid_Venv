import random
from string import ascii_letters, digits, whitespace, punctuation
import os
from gidtools.gidfiles import bytes2human
from zipfile import ZipFile, ZIP_LZMA
all_select = list(ascii_letters) + list(map(str, digits)) + list(whitespace) + list(punctuation) + list(ascii_letters) + list(ascii_letters) + list(ascii_letters) + list(punctuation) + list(ascii_letters) + list(ascii_letters) + list(ascii_letters)
file = "file_to_download_3.zip"

# with open(file, 'w') as f:
#     for i in range(900):
#         f.write("this is my teststring\n")

with ZipFile(file, 'w', ZIP_LZMA) as zippy:
    for file in os.scandir(os.getcwd()):
        if file.is_file() and file.name != 'rrr.py' and not file.name.endswith('.zip'):
            zippy.write(file.path, file.name)

size = os.stat(file).st_size
print(bytes2human(size, annotate=True))
print(size)
