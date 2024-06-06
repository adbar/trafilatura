import json
import os

from evaldata import EVAL_PAGES


# check if all entries have a corresponding html
print('MISSING HTMLS')
for k, v in EVAL_PAGES.items():
    filename = v['file']
    if not os.path.exists(f'eval/{filename}') and \
        not os.path.exists(f'cache/{filename}'):
        print(k, filename)

# check if all html appear in evalpages file
def collect_file_values(d, file_set=None):
    if file_set is None:
        file_set = set()
    if isinstance(d, dict):
        for k, v in d.items():
            if k == 'file':
                file_set.add(v)
            elif isinstance(v, dict):
                collect_file_values(v, file_set)
    return file_set

filenames = collect_file_values(EVAL_PAGES)
print(len(filenames))
print('\nMISSING ENTRIES')

def check_for_html_in_evaldata(htmldir):
    files = os.listdir(htmldir)
    print('\n', htmldir, len(files))
    for f in files:
        if not f in filenames:
            print(f)

check_for_html_in_evaldata('eval/')
check_for_html_in_evaldata('cache/')

# create json file
with open('evaldata.json', 'w', encoding='utf-8') as f:
    json.dump(EVAL_PAGES, f, indent=4)
