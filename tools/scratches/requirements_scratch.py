from requirements import parse
from gidtools.gidfiles import readit, writeit, pathmaker
from inspect import getmembers

from pkg_resources import parse_requirements
req_file = r"D:\Dropbox\hobby\Modding\Programs\Github\My_Repos\Gid_Venv\tools\scratches\scratch_requirements.txt"

data = readit(req_file)

x = parse(data)
for i in x:
    print(i.extras)
