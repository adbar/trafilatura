from pathlib import Path
import re, json, codecs

path = Path('benchmark/dataset_cleaned')
path_o = Path('benchmark/ground/output_pzh.json')

o_result = {}

for i in path.glob('*'):
    try:
        with open(i, 'r', encoding='latin-1') as f:
            output = f.read()
            id = i.name.split('.')[0]
            # print(repr(result))
            o_result[id] = {"articleBody": output}
    except UnicodeDecodeError:
        print(id)
        # o_result[id] = {"articleBody": result.decode('latin-1')}

# print(o_result)
with open(path_o, 'w+', encoding='latin-1') as f:
    json.dump(o_result, f, indent=4, ensure_ascii=False)
