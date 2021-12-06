from bs4 import BeautifulSoup, SoupStrainer
import requests
import re
import lxml
from functools import reduce
import itertools

headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}

channel = requests.get(
    'https://dreamcargiveaways.co.uk/current-competitions/', timeout=10, headers=headers).text

productSelector = {
    "container": '',
    "title": '',
    "price": '',
    "tickets": '',
    "maxPP": '',
    "timeRemaining": '',
}

passedProps = {
    "url": 'https://dreamcargiveaways.co.uk/current-competitions/',
    "title": 'Audi RS6 OR Porsche 911 Carrera S OR £100,000 Tax Free',
    "price": '11.98',
    "tickets": '1856 Remaining',
    "maxPP": 'max. 12pp',
    "timeRemaining": '3hrs',
}

soup = BeautifulSoup(channel, 'lxml')
titleFound = soup.find_all(text=re.compile(passedProps["title"]))
el = titleFound[0].parent
productSelector['title'] = f"{el.name}.{'.'.join(el['class'])}"


def findParentContainer(element):
    return element.parent


def determineElementClasses(list1, list2):
    return list(itertools.filterfalse(lambda x: x not in list2, list1))


for x in range(0, 4):
    el = findParentContainer(el)
    products = list(filter(lambda e: e != '\n', el.contents))
    elementTypes = list(map(lambda e: e.name, products))
    elementClasses = list(map(lambda e: e['class'], products))
    if len(elementTypes) > 1 and elementTypes.count(elementTypes[0]) == len(elementTypes):
        acc = []
        for i, cssClass in enumerate(elementClasses):
            if i == 0 and acc != elementClasses[i + 1]:
                acc = elementClasses[i + 1]
            acc = determineElementClasses(cssClass, acc)
        if len(acc) > 0:
            productSelector["container"] = f"{elementTypes[0]}.{'.'.join(acc)}"
            break

allProds = soup.select(productSelector["container"])
originalProd = None
for prod in allProds:
    if prod.find(text=re.compile(passedProps["title"])):
        originalProd = prod
        break

print(originalProd)

for item in passedProps.items():
    if item[0] == "url" or productSelector[item[0]] != "":
        continue
    print(item)
    itemKey = item[0]
    itemValue = item[1]
    elFound = originalProd.find(text=re.compile(passedProps[itemKey]))
    if elFound == None:
        continue
    print(elFound.parent, 'found')


# TODO
# Create recursive function to find all elements with the same class
# based on elementClasses list of lists
# list(itertools.filterfalse(lambda x: x not in list2, list1))
# Determine if/how to find product container if there is only one product on the site
