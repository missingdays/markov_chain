
from lxml import html
import requests

page = requests.get('https://ru.wikipedia.org/wiki/%D0%A1%D0%BF%D0%B8%D1%81%D0%BE%D0%BA_%D1%8D%D0%BF%D0%B8%D0%B7%D0%BE%D0%B4%D0%BE%D0%B2_%D1%82%D0%B5%D0%BB%D0%B5%D1%81%D0%B5%D1%80%D0%B8%D0%B0%D0%BB%D0%B0_%C2%AB%D0%9A%D0%BB%D0%B8%D0%BD%D0%B8%D0%BA%D0%B0%C2%BB')
tree = html.fromstring(page.content)

# Dirty query that just works :P
text = tree.xpath('//td[@colspan=5]/text()')

with open('../example/Scrubs.ru.txt', 'w') as f:
    for l in text:
        for c in l:
            f.write(c)

            if c == '.':
                f.write(' ')
    f.write(' ')
