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

url = 'https://piensoymascotas.com/pienso-natural/3445-5540-orijen-regional-red-cat.html#/1428-formato-saco_de_54_kg'
url2 = 'https://piensoymascotas.com/pienso-natural/3445-5539-orijen-regional-red-cat.html#/1433-formato-saco_de_18_kg'

piensosYMascotasLinks = [
    'https://piensoymascotas.com/pienso-sin-cereales/3949-7510-acana-prarie-poultry.html#/1015-formato-saco_de_114_kg',
    'https://piensoymascotas.com/pienso-sin-cereales/3949-7511-acana-prarie-poultry.html#/1198-formato-saco_de_17_kg',
    'https://piensoymascotas.com/pienso-sin-cereales/3950-7515-acana-wild-coast.html#/1015-formato-saco_de_114_kg',
    'https://piensoymascotas.com/pienso-sin-cereales/3950-7516-acana-wild-coast.html#/1198-formato-saco_de_17_kg',
    ]

piensosYMascotasPrices = []

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
    product = {
        'name': name,
        'qty': kgs,
        'price': price,
        'link': url,
    }
    piensosYMascotasPrices.append(product)
    #print(piensosYMascotasPrices)


def getPiensosYMascotasPrices():
    start_time = time.time()
    print('\n>A coletar dados de piensosymascotas.com...')
    for link in piensosYMascotasLinks:
        soup = get_data(link)
        parse(soup, link)
    elapsed = time.time() - start_time
    print('\n>Dados de piensosymascotas.com colectados. Duração total: ', strftime("%M:%S", gmtime(elapsed)), 'minutos.')
    return


def run():
    getPiensosYMascotasPrices()
    xlsxPiensosYMascotas()


def csvPiensosYMascotas():
    file = open('piensosYMascotas.csv', 'w', newline='')
    with file:
        # identifying header
        header = ['name', 'qty', 'price', 'link']
        writer = csv.DictWriter(file, fieldnames=header)
        writer.writeheader()
        for item in piensosYMascotasPrices:
            writer.writerow(item)
    piensosYMascotasPrices.clear()
    return

def xlsxPiensosYMascotas():
    pd.DataFrame(piensosYMascotasPrices).to_excel('piensosYMascotas.xlsx', header=True, index=False)
    piensosYMascotasPrices.clear()
    return

"""
getPiensosYMascotasPrices()
csvPiensosYMascotas()

soup = get_data(url)
parse(soup, url)
"""

if __name__ == '__main__':
    getPiensosYMascotasPrices()
    xlsxPiensosYMascotas()

