from bs4 import BeautifulSoup, SoupStrainer
import requests
import re
import lxml
from functools import reduce
import itertools

headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}

channel = requests.get(
    'https://dreamcargiveaways.co.uk/current-competitions/audi-rs6-or-porsche-911-carrera-s-or-100000-tax-free/', timeout=10, headers=headers).text

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

soup = BeautifulSoup(channel, 'lxml')
body = soup.find('body')
titleFound = body.find_all(text=re.compile(passedProps["title"]))
print(titleFound)
el = titleFound[0].parent
print(el)
productSelector['title'] = f"{el.name}.{'.'.join(el['class'])}"
print(productSelector)


# TODO
# Figure out best way to show a user which piece of information would be best
# e.g. discourage using updating values such as ticking countdowns instead
# use static draw date times & calculate the time remaining client side
# Determine whether to scrape the data of all product thumbnails first
# or whether to scrape thumbnails & full product page at the same time
