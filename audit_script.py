import os
os.chdir(r'C:\Users\60113\Documents\Codex\2026-06-13\https-v-douyin-com-tqasgidtyku-100\trafilatura')

files = ['trafilatura/downloads.py', 'trafilatura/spider.py', 'trafilatura/utils.py']
for f in files:
    print('=== ' + f + ' ===')
    with open(f, 'r', encoding='utf-8') as fh:
        content = fh.read()
        print(content[:2000])
    print()
