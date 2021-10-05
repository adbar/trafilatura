
import os
import time

from evaldata import EVAL_PAGES
from trafilatura import bare_extraction

TEST_DIR = os.path.abspath(os.path.dirname(__file__))



def load_document_binary(filename):
    '''load mock page from samples'''
    mypath = os.path.join(TEST_DIR, 'cache', filename)
    if not os.path.isfile(mypath):
        mypath = os.path.join(TEST_DIR, 'eval', filename)
    #if not os.path.isfile(mypath):
    #    mypath = os.path.join(TEST_DIR, 'additional', filename)
    with open(mypath, 'rb') as inputf:
        htmlstring = inputf.read()
    return htmlstring


def run_trafilatura(htmlstring):
    '''run trafilatura (without fallback) on content'''
    return bare_extraction(htmlstring, output_format='python')


i = 0
correct = 0
start = time.time()

for item in EVAL_PAGES:
    if len(EVAL_PAGES[item]['file']) == 0:
        continue
    if not 'author' in EVAL_PAGES[item] or len(EVAL_PAGES[item]['author']) < 1:
        continue
    author_gold = EVAL_PAGES[item]['author']
    i += 1
    # print(EVAL_PAGES[item]['file'])
    htmlstring = load_document_binary(EVAL_PAGES[item]['file'])
    if htmlstring is None:
        continue
    try:
        result = run_trafilatura(htmlstring)
    # exception in some past versions
    except AttributeError:
        result = None
    if result is None:
        continue
    if 'author' in result and result['author'] == author_gold:
        correct += 1

print('exec. time:', '%.2f' % (time.time() - start))
print('total, correct, percentage:')
print(i, correct, '%.2f' % ((correct/i)*100))

