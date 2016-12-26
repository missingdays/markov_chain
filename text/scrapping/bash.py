# -*- coding: utf-8 -*-

from lxml import html
import requests
import os

os.remove('../example/bash.ru.txt')

for i in range(100, 120):
    page = requests.get("http://bash.im/index/{}".format(i))

    content = page.text.encode('utf-8').decode('utf-8')

    #print(content)

    tree = html.fromstring(content)

    text = tree.xpath('//div[@class="text"]/text()')

    with open('../example/bash.ru.txt', 'a') as f:
        for l in text:
            for c in l:
                if c == ')' or c == '(':
                    continue

                f.write(c)
            f.write('\n')
        f.write('\n')
