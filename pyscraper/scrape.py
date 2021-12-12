from bs4 import BeautifulSoup
import requests
import re
import itertools

headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}

channel = requests.get(
    'https://dreamcargiveaways.co.uk/current-competitions/', timeout=10, headers=headers).text

productSelector = {
    "container": '',
    "title": '',
    "price": '',
    "ticketsRemaining": '',
    "maxPP": '',
    "timeRemaining": '',
}

baseUrl = 'https://dreamcargiveaways.co.uk'
passedProps = {
    "url": 'https://dreamcargiveaways.co.uk/current-competitions/',
    "title": 'Mercedes-Benz GLC63S & £5000 or £70,000',
    "price": '4.29',
    "ticketsRemaining": '25898 Remaining',
    "maxPP": 'max. 30pp',
    "timeRemaining": '+7d',
}

for prop in passedProps.items():
    passedProps[prop[0]] = re.escape(prop[1])

soup = BeautifulSoup(channel, 'lxml')
titleFound = soup.find(text=re.compile(passedProps["title"]))
el = titleFound.parent
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

print(originalProd, 'original prod')

for item in passedProps.items():
    if item[0] == "url" or productSelector[item[0]] != "":
        continue
    itemKey = item[0]
    itemValue = item[1]
    if not passedProps[itemKey]:
        continue
    elFound = originalProd.find(text=re.compile(passedProps[itemKey]))
    if elFound == None:
        continue
    productSelector[itemKey] = f"{elFound.parent.name}.{'.'.join(elFound.parent['class'])}"
    print(elFound.parent, 'found')

print(productSelector, 'FINAL')

listings = soup.select(productSelector["container"])

dataRetrieved = []

for listing in listings:
    listingItem = {}
    linkTest = listing.find('a')
    listingItem["url"] = baseUrl + linkTest['href']
    print(linkTest, 'link test')
    for item in productSelector.items():
        itemKey = item[0]
        itemValue = item[1]
        if itemKey == "container" or not itemValue:
            continue
        listingSelected = listing.select_one(itemValue)
        listingItem[itemKey] = listingSelected and listingSelected.string and listingSelected.string.strip()
    dataRetrieved.append(listingItem)

print(dataRetrieved)

# TODO
# Determine if/how to find product container if there is only one product on the site
# Determine how to add prompts for users on N/A or not found values
# Convert to flask API
# Review efficiency
# Check best way to achieve concurrent requests through FE
# Use multiple API calls with Promise.race?

# Determine how to get price/info when tag contains more than one child. Swap to dictionary
# for each productSelector? E.g. { element: 'span', class: 'price' } for use with get text?

# Clean up trailing ands in final for, create better error handling for this
