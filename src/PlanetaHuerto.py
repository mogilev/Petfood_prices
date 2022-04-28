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

# testlink = 'https://petness.pt//p/37325/suntory-torys-classic'

url = 'https://www.planetahuerto.pt/venda-racao-para-caes-adultos-light-fit-acana-114-kg_06543'

planetaHuertoPtLinks = [
    'https://www.planetahuerto.pt/venda-classic-prairie-poultry-acana_37659',
    'https://www.planetahuerto.pt/venda-classic-prairie-poultry-acana_37659',
    'https://www.planetahuerto.pt/venda-puppy-junior-acana_06536',
    'https://www.planetahuerto.pt/venda-adult-heritage-cobb-chicken-greens-frango-y-verduras-acana_06540',
    ]

planetaHuertoEsLinks = [
    'https://www.planetahuerto.es/venta-classic-prairie-poultry-acana_37659',
    'https://www.planetahuerto.es/venta-classic-prairie-poultry-acana_37659',
    'https://www.planetahuerto.es/venta-puppy-junior-acana_06536',
    'https://www.planetahuerto.es/venta-adult-heritage-cobb-chicken-greens-pollo-y-verduras-acana_06540',
    ]

planetahuertoPrices = []


def get_data(url):
    r = requests.get(url, headers=headers)
    soup = BeautifulSoup(r.text, 'html.parser')
    return soup


def parse(soup, url):
    time.sleep(1)
    url = url
    planetaHuertoProduct = {
        'name': soup.find('h1', {'id': 'js-product-card-name'}).text.replace('\n', '').replace('\t', '').strip(),
        'availability': soup.find('span', {'id': 'js-in-stock-label'}).text.replace('\n', '').replace(' ', '').strip(),
        'price': soup.find('span', {'id': 'js-product-price'}).text.replace('€', '').replace(u'\xa0', u'').strip(),
        'link': url,
    }
    planetahuertoPrices.append(planetaHuertoProduct)
    #print(planetaHuertoProduct)
    return



def getPlanetaHuertoPtPrices():
    start_time = time.time()
    print('\n>A coletar dados de planetaHuerto.pt...')
    for link in planetaHuertoPtLinks:
        soup = get_data(link)
        parse(soup, link)
    elapsed = time.time() - start_time
    print('\n>Dados de planetaHuerto.pt colectados. Duração total: ', strftime("%M:%S", gmtime(elapsed)), 'segundos.')
    return

def getPlanetaHuertoEsPrices():
    start_time = time.time()
    print('\n>A coletar dados de planetaHuerto.es...')
    for link in planetaHuertoPtLinks:
        soup = get_data(link)
        parse(soup, link)
    elapsed = time.time() - start_time
    print('\n>Dados de planetaHuerto.es colectados. Duração total: ', strftime("%M:%S", gmtime(elapsed)), 'minutos.')
    return

def run():
    getPlanetaHuertoPtPrices()
    xlsxPetnessPt()

    getPlanetaHuertoEsPrices()
    xlsxPetnessEs()


def csvPlanetaHuertoPt():
    file = open('planetaHuertoPt.csv', 'w', newline='')
    with file:
        # identifying header
        header = ['name', 'availability', 'price', 'link']
        writer = csv.DictWriter(file, fieldnames=header)
        writer.writeheader()
        for item in planetahuertoPrices:
            writer.writerow(item)
    planetahuertoPrices.clear()
    return

def csvPlanetaHuertoEs():
    file = open('planetaHuertoEs.csv', 'w', newline='')
    with file:
        # identifying header
        header = ['name', 'availability', 'price', 'link']
        writer = csv.DictWriter(file, fieldnames=header)
        writer.writeheader()
        for item in planetahuertoPrices:
            writer.writerow(item)
    planetahuertoPrices.clear()
    return

def xlsxPetnessPt():
    pd.DataFrame(planetahuertoPrices).to_excel('planetaHuertoPt.xlsx', header=True, index=False)
    planetahuertoPrices.clear()
    return

def xlsxPetnessEs():
    pd.DataFrame(planetahuertoPrices).to_excel('planetaHuertoEs.xlsx', header=True, index=False)
    planetahuertoPrices.clear()
    return

#getPlanetaHuertoPtPrices()
#csvPlanetaHuerto()

"""
soup = get_data(url)
parse(soup, url)
"""

if __name__ == '__main__':
    getPlanetaHuertoPtPrices()
    xlsxPetnessPt()
    
    getPlanetaHuertoEsPrices()
    xlsxPetnessEs()
