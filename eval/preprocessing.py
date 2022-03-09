from pathlib import Path
import re, json, codecs

path = Path('benchmark/zh-cleaned/zh-cleaned')
path_o = Path('benchmark/ground/output_zh.json')

o_result = {}

for i in path.glob('*'):
    with open(i, 'rb') as f:
        output = f.read()
        result = output.split(b'\n')[1:]
        result = b"\n".join(result).strip()
        result = re.sub(rb'(<\w>)', b'', result)
        id = i.name.split('-')[0]
        # print(repr(result))
        try:
            o_result[id] = {"articleBody": result.decode('latin-1')}
        except UnicodeDecodeError:
            print(id)
            # o_result[id] = {"articleBody": result.decode('latin-1')}

# print(o_result)
with open(path_o, 'w+', encoding='latin-1') as f:
    json.dump(o_result, f, indent=4, ensure_ascii=False)
