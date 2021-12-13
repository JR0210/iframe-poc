from bs4 import BeautifulSoup
import requests

headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}

channel = requests.get(
    'https://dreamcargiveaways.co.uk/current-competitions/', timeout=10, headers=headers).text

baseUrl = 'https://dreamcargiveaways.co.uk'

soup = BeautifulSoup(channel, 'lxml')

allProds = soup.select('li.product.type-product.product-type-competition')

for x in allProds:
    test = x.select('span.woocommerce-Price-amount.amount')
    print(test)
    if len(test) > 1:
        formattedtest = list(map(lambda e: e.get_text().strip(), test))
        print(formattedtest[0])
        print(formattedtest[0].isnumeric())
        print(min(formattedtest), 'min?')
