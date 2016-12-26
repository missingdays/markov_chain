
from lxml import html
import requests

page = requests.get('http://poetrylibrary.ru/stixiya/brodskij-1.html')

tree = html.fromstring(page.content)

# Dirty query that just works :P
text = tree.xpath('//mytag[@var="text"]/text()')

with open('../example/Brodsky.ru.txt', 'w') as f:
    for l in text:
        for c in l:
            f.write(c)

            if c == '.':
                f.write(' ')
    f.write(' ')
