from re import Scanner, IGNORECASE, DOTALL, MULTILINE
from pprint import pprint
from time import time
from gidtools.gidfiles import writejson

with open(r"D:\Dropbox\hobby\Modding\Programs\Github\My_Repos\Arma_class_parser_utility\temp\config_dumps\rhs_3cb_faa_unsung_config_dump.cpp", 'r') as f:
    content = f.read()


scanner = Scanner([
    (r'class bin\\config.bin', lambda x, y:('stupid', y)),
    (r'class\s+\w+(?!\:)(?=\n)', lambda x, y: ('class_single', y.replace('class', '').strip())),
    (r'^\t{2}class\s+.*?\:.*?(?=\n)', lambda x, y: ('class_child_parent', (y.replace('\t\tclass', '').split(':')[0].strip(), y.replace('class', '').split(':')[-1].strip()))),
    (r'class.*?\:\s+\w+(?=\n)', lambda x, y:('other_stupid', y)),
    (r'\w+\[\]\s+\=.*?(?=\n)', lambda x, y:('weirdattr', y)),
    (r'\w+\s+\=.*?(?=\n)', lambda x, y:('attr', y)),
    (r'[\{|\}]', lambda x, y: ('curly_stuff', y)),
    (r'\;', lambda x, y:('semicolon', '')),
    (r'\n', lambda x, y:('newline', '')),
    (r'\s+', lambda y, x: ('whitespace', ''))], flags=IGNORECASE | MULTILINE)


def _make_pairs(in_data):
    _out = {}
    par = "NO_SECTION"
    _out[par] = []
    for res in scanner.scan(in_data):

        for tok, res_res in res:
            # if tok in ['class_single', 'class_child_parent'] and 'cfg' in res_res.casefold():
            #     _out[par].append((tok, res_res))
            if tok == 'class_single' and 'cfg' in res_res.casefold() and not res_res.casefold().startswith('export'):
                par = res_res
                if par not in _out:
                    _out[par] = []
            if tok == 'class_child_parent':
                print(res_res)
                _out[par].append((tok, res_res))
    return _out


writejson(_make_pairs(content), 'teghbj.json')
