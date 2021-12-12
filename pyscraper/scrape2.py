from bs4 import BeautifulSoup, SoupStrainer
import re
from dateutil.parser import parse

import codecs

data = codecs.open("productPage.html", 'r', 'utf-8')

headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}

# channel = requests.get(
#     'https://dreamcargiveaways.co.uk/current-competitions/audi-rs6-or-porsche-911-carrera-s-or-100000-tax-free/', timeout=10, headers=headers).text

productSelector = {
    "container": '',
    "title": '',
    "price": '',
    "tickets": '',
    "maxPP": '',
    "timeRemaining": '',
}

passedProps = {
    "url": 'https://dreamcargiveaways.co.uk/current-competitions/audi-rs6-or-porsche-911-carrera-s-or-100000-tax-free/',
    "title": 'Audi RS6 OR Porsche 911 Carrera S OR £100,000 Tax Free',
    "price": '11.98',
    "tickets": '1856 Remaining',
    "maxPP": 'max. 12pp',
    "timeRemaining": '3hrs',
}

onlyBody = SoupStrainer("body")
data = data.read().replace('&nbsp;', ' ')
body = BeautifulSoup(data, 'lxml', parse_only=onlyBody)
# print(body)
titleFound = body.find_all(text=re.compile(passedProps["title"]))
# print(titleFound)
el = titleFound[0].parent
# print(el)
productSelector['title'] = f"{el.name}.{'.'.join(el['class'])}"
# print(productSelector)

# INITIAL FIND DATE CLASS & TAG
dateTest = body.find(text=re.compile(
    'The draw date for this competition is 05/12/2021 8:00 pm'))
dateParent = dateTest.parent

# Selector to use after initial scrape to get data using user passed data
# selector - span.\"\\"s1\\"\"
# Find all then use date parse in each until date is found
allParentSelectors = body.find_all(
    dateParent.name, class_=dateParent['class'][0])

print(allParentSelectors)
print(dateParent.name)
print(dateParent['class'][0])


dateParseTest = 'The draw date for this competition is&nbsp;05/12/2021 8:00 pm'
dateParseTest = dateParseTest.replace('&nbsp;', ' ')
print(dateParseTest)
drawDate = parse(dateParseTest, dayfirst=True, fuzzy=True)
print(drawDate)
print(drawDate.date())


# TODO
# Figure out best way to show a user which piece of information would be best
# e.g. discourage using updating values such as ticking countdowns instead
# use static draw date times & calculate the time remaining client side
# Determine whether to scrape the data of all product thumbnails first
# or whether to scrape thumbnails & full product page at the same time

# For dates etc where data from class selector is not only data needed
# use CSS selector plus XPath with regex? Or just regex through class text
