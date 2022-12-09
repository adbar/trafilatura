from trafilatura import fetch_url, extract, baseline, bare_extraction
from trafilatura.feeds import find_feed_urls
from trafilatura.spider import focused_crawler
from lxml import html
import sys

document = fetch_url('https://www.naver.com')
doc_dict = bare_extraction(document)
tree = html.fromstring(document)
links = find_feed_urls('https://www.theguardian.com')
lxml_object, text, length = baseline(document)
xml = extract(document, output_format='xml')
to_visit, known_urls = focused_crawler(
    'https://telebasel.ch/', max_seen_urls=3)


class Tra:

    def __init__(self):
        self.p = {'bare_extraction', 'tree', 'find_feed_urls',
            'baseline', 'Web crawling', 'xml'}
        self.n = {1: 'bare_extraction', 2: 'tree', 3: 'find_feed_urls',
            4: 'baseline', 5: 'Web crawling', 6: 'xml'}

        self.inputurl = 'https://www.naver.com'

    def url(self):
        print('[Url을 입력해주세요 https://]')
        while True:
            try:
                input('Url:')
            except Exception as e:
                print(e)
                continue
            else:
                print('입력한 Url:', self.inputurl)
                print()
                break

    def showmode(self):

        print('[원하는 크롤링 모드을 기입해주세요]')
        print()
        print('1:bare_extraction')
        print('2:tree')
        print('3:find_feed_urls')
        print('4:baseline')
        print('5:Web crawling')
        print('6:xml')

        print()

    def print(self):

        try:
            n = int(input('번호선택(종료:0):'))

        except Exception as e:
            print(e)
        else:
            if n == 0:
                return False

            if n == 1:

                print(links)
                print()
                loadlinkstxt = input("출력물을 저장하시겠습니까? (yes,no): ")
                if (loadlinkstxt == 'yes'):
                    sys.stdout = open('link.txt', 'w')
                    print(links)
                    sys.stdout.close()

            elif n == 2:

                print(doc_dict.keys())
                loaddoc_dict = input("출력물을 저장하시겠습니까? (yes,no): ")
                if (loaddoc_dict == 'yes'):
                    sys.stdout = open('doc_dict.txt', 'w')
                    print(doc_dict.keys())
                    sys.stdout.close()
            elif n == 3:

                print(tree)
                loadtree = input("출력물을 저장하시겠습니까? (yes,no): ")
                if (loadtree == 'yes'):
                    sys.stdout = open('tree.txt', 'w')
                    print(tree)
                    sys.stdout.close()
            elif n == 4:
                print(text)
                loadtext = input("출력물을 저장하시겠습니까? (yes,no): ")
                if (loadtext == 'yes'):
                    sys.stdout = open('text.txt', 'w')
                    print(text)
                    sys.stdout.close()
            elif n == 5:
                print('\n.'.join(list(to_visit)[:5]))
                print('---')
                print('\n.'.join(list(known_urls)[:5]))
                loadto_visit = input("출력물을 저장하시겠습니까? (yes,no): ")
                if (loadto_visit == 'yes'):
                    sys.stdout = open('to_visit.txt', 'w')
                    print('\n.'.join(list(to_visit)[:5]))
                    print('---')
                    print('\n.'.join(list(known_urls)[:5]))
                    sys.stdout.close()

            elif n == 6:
                print(xml)
                loadxml = input("출력물을 저장하시겠습니까? (yes,no): ")
                if (loadxml == 'yes'):
                    sys.stdout = open('xml.txt', 'w')
                    print(xml)
                    sys.stdout.close()
            else:
                print("잘못된 번호")

        return True


z = Tra()
z.url()
z.showmode()


while z.print():
    print()
    z.showmode()

print('웹 크롤링 종료')
