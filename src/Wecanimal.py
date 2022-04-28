import requests
from bs4 import BeautifulSoup
import csv
import pandas as pd
import time
from time import gmtime
from time import strftime

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36'
}

url = 'https://wecanimal.pt/acana-regional-gato/7451-91202-acana-cat-homestead-harvest.html#/896-formato-bolsa_de_340_gr'
url2 = 'https://wecanimal.pt/acana-regional-gato/7451-91203-acana-cat-homestead-harvest.html#/1433-formato-saco_de_18_kg'

wecanimalLinks = [
    'https://wecanimal.pt/racao-sem-cereais/3949-7510-acana-prarie-poultry.html#/1015-formato-saco_de_114_kg',
    'https://wecanimal.pt/racao-sem-cereais/3949-7511-acana-prarie-poultry.html#/1198-formato-saco_17_kg',
    'https://wecanimal.pt/racao-sem-cereais/3950-7515-acana-wild-coast.html#/1015-formato-saco_de_114_kg',
    'https://wecanimal.pt/racao-sem-cereais/3950-7516-acana-wild-coast.html#/1198-formato-saco_17_kg',
    'https://wecanimal.pt/racao-sem-cereais/3951-7521-acana-classic-red.html#/1198-formato-saco_17_kg',
    'https://wecanimal.pt/racao-sem-cereais/3012-4250-acana-puppy-and-junior.html#/1198-formato-saco_17_kg',
    'https://wecanimal.pt/racao-sem-cereais/3013-4253-acana-puppy-large-breed.html#/1198-formato-saco_17_kg',
    'https://wecanimal.pt/racao-sem-cereais/3014-4257-adult-small-breed.html#/25-formato-saco_de_6_kg',
    'https://wecanimal.pt/caes/3023-4293-acana-adult-dog.html#/1198-formato-saco_17_kg',
    'https://wecanimal.pt/racao-sem-cereais/3022-4284-acana-adult-large-breed.html#/1198-formato-saco_17_kg',
    'https://wecanimal.pt/racao-sem-cereais/3020-4275-acana-light-fit-all-breeds.html#/1015-formato-saco_de_114_kg',
    'https://wecanimal.pt/racao-sem-cereais/3021-4281-acana-senior-all-breeds.html#/1015-formato-saco_de_114_kg',
    'https://wecanimal.pt/racao-sem-cereais/3001-7919-acana-wild-prairie.html#/1015-formato-saco_de_114_kg',
    'https://wecanimal.pt/racao-sem-cereais/3003-4211-acana-pacifica.html#/1015-formato-saco_de_114_kg',
    'https://wecanimal.pt/racao-sem-cereais/3158-90981-acana-wild-prairie-cat.html#/289-formato-saco_de_45_kg',
    'https://wecanimal.pt/pienso-classic/2995-4179-orijen-adult-dog.html#/1015-formato-saco_de_114_kg',
    'https://wecanimal.pt/racao-sem-cereais/2998-4191-orijen-six-fish.html#/1015-formato-saco_de_114_kg',
    'https://wecanimal.pt/racao-natural/3440-5517-orijen-cat-kitten.html#/1428-formato-saco_de_54_kg',
    ]

wecanimalPrices = []

def get_data(url):
    r = requests.get(url, headers=headers)
    soup = BeautifulSoup(r.text, 'html.parser')
    return soup


def parse(soup, url):
    price = soup.find('span', {'itemprop': 'price'}).text.replace('€', '').replace(u'\xa0', u'').strip()
    name = soup.find('h1', {'class': 'tvproduct-content-title hidden-sm-down'}).text
    title = soup.find('title').text
    url = url
    eraser = ' de '
    kgs = title.split(eraser, 1)[-1]
    quantities = []
    product = {
        'name': name,
        'qty': kgs,
        'price': price,
        'link': url,
    }
    wecanimalPrices.append(product)
    #print(wecanimalPrices)


def getWecanimalPrices():
    start_time = time.time()
    print('\n>A coletar dados de wecanimal.pt...')
    for link in wecanimalLinks:
        soup = get_data(link)
        parse(soup, link)
    elapsed = time.time() - start_time
    print('\n>Dados de wecanimal.pt colectados. Duração total: ', strftime("%M:%S", gmtime(elapsed)), 'minutos.')
    return

def run():
    getWecanimalPrices()
    xlsxWecanimal()


def csvWecanimal():
    file = open('wecanimal.csv', 'w', newline='')
    with file:
        # identifying header
        header = ['name', 'qty', 'price', 'link']
        writer = csv.DictWriter(file, fieldnames=header)
        writer.writeheader()
        for item in wecanimalPrices:
            writer.writerow(item)
    wecanimalPrices.clear()
    return

def xlsxWecanimal():
    pd.DataFrame(wecanimalPrices).to_excel('wecanimal.xlsx', header=True, index=False)
    wecanimalPrices.clear()
    return

"""
getWecanimalPrices()
csvWecanimal()

soup = get_data(url2)
parse(soup, url2)

"""
if __name__ == '__main__':
    getWecanimalPrices()
    xlsxWecanimal()

