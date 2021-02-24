import random
from string import ascii_letters, digits, whitespace, punctuation
import os
from gidtools.gidfiles import bytes2human
all_select = list(ascii_letters) + list(map(str, digits)) + list(whitespace) + list(punctuation) + list(ascii_letters) + list(ascii_letters) + list(ascii_letters) + list(punctuation) + list(ascii_letters) + list(ascii_letters) + list(ascii_letters)
file = "file_to_download_1.py"

with open("file_to_download_1.py", 'w') as f:
    f.write('x = """')
    for i in range(900):
        f.write("this is my teststring\n")
    f.write('"""')


size = os.stat(file).st_size
print(bytes2human(size, annotate=True))
