from bs4 import BeautifulSoup, SoupStrainer
import requests
import re
import lxml
from functools import reduce

headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}

channel = requests.get(
    'https://dreamcargiveaways.co.uk/current-competitions/', timeout=10, headers=headers).text
soup = BeautifulSoup(channel, 'lxml')
titleFound = soup.find_all(text=re.compile(
    'Audi RS6 OR Porsche 911 Carrera S OR £100,000 Tax Free'))
el = titleFound[0].parent


def findParentContainer(element):
    return element.parent


for x in range(0, 4):
    el = findParentContainer(el)

    # TODO
    # Check for title.children - bs4Element.name for li etc
    # Check for title.children['class'] - bs4Element[class] for most matching classes
    # if all(title.children):
    #     print(title.children)
    #     break
    print(x)
    if x == 3:
        print(el.contents)
