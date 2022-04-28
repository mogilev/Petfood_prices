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


url = 'https://www.miscota.pt/gatos/acana/p-175696'
url2 = 'https://www.miscota.pt/gatos/acana/p-187821'

"""
Colocar opções:
    0 - Necessário 11 e 17kgs
    1 - 17 kgs
    2 - 11 kgs
    3 -  6 kgs
    4 -  5,4 kgs
    5 -  4,5 kgs
"""
miscotaLinks = [
    ['https://www.miscota.pt/caes/acana/p-114650',0],
    ['https://www.miscota.pt/caes/acana/classic-red-116935',1],
    ['https://www.miscota.pt/caes/acana/adult-small-breed-116923-117070',3],
    ['https://www.miscota.pt/gatos/acana/p-175696',5],
    ['https://www.miscota.pt/caes/orijen/p-130615',2],
    ['https://www.miscota.pt/gatos/orijen/p-123282',4],
    ]

miscotaEsLinks = [
    ['https://www.miscota.es/perros/acana/p-114650',0],
    ['https://www.miscota.es/perros/acana/p-69874',1],
    ['https://www.miscota.es/perros/acana/adult-small-breed-340-gr-117070',3],
    ['https://www.miscota.es/perros/acana/adult-large-breed',1],
    ['https://www.miscota.es/perros/acana/p-69871',2],
    ['https://www.miscota.es/gatos/acana/wild-prairie-cat',5],
    ['https://www.miscota.es/gatos/orijen/p-123282',4],
    ]

miscotaPrices = []


def get_data(url):
    r = requests.get(url, headers=headers)
    soup = BeautifulSoup(r.text, 'html.parser')
    return soup

def parse(soup, url, option):
    name = soup.find('h1', {'class': 'product-name'}).text.strip()
    results = soup.find('div', {'class':'product-variation--size'}).find_all('li', {'itemprop':'offers'})
    url=url

    quantities = []
    for result in results:
        miscotaProduct = {
            'name': name,
            'price': result.find('span', {'class': 'variation-price'}).text.replace('€','').strip(),
            'quantity': result.find('span', {'class': 'variation-name'}).text.strip(),
            'sku': result.find('meta', {'itemprop': 'sku'})['content'],
            'link': url,
            }
        quantities.append(miscotaProduct)

    if option == 0:
        for item in quantities:
            if item['quantity'] == '11,4 Kg':
                miscotaPrices.append(item)
                #print(item) #print de teste
        for item in quantities:
            if item['quantity'] == '17 Kg':
                miscotaPrices.append(item)
                #print(item)  # print de teste

    if option == 1:
        for item in quantities:
            if item['quantity'] == '17 Kg':
                miscotaPrices.append(item)
                #print(item)  # print de teste

    if option == 2:
        for item in quantities:
            if item['quantity'] == '11,4 Kg' or item['quantity'] == '11,4 kg':
                miscotaPrices.append(item)
                #print(item)  # print de teste

    if option == 3:
        for item in quantities:
            if item['quantity'] == '6 Kg':
                miscotaPrices.append(item)
                #print(item)  # print de teste

    if option == 4:
        for item in quantities:
            if item['quantity'] == '5,4 Kg' or item['quantity'] == '5,4 KG':
                miscotaPrices.append(item)
                #print(item)  # print de teste

    if option == 5:
        for item in quantities:
            if item['quantity'] == '4,5 Kg' or item['quantity'] == '4,5 KG':
                miscotaPrices.append(item)
                #print(item)  # print de teste


def getMiscotaPtPrice():
    start_time = time.time()
    print('\n>A coletar dados de miscota.pt..')
    for link in miscotaLinks:
        siteLink = link[0]
        option = link[1]
        soup = get_data(siteLink)
        parse(soup, siteLink, option)
    xlsxMiscotaPt()
    elapsed = time.time() - start_time
    print('\n>Dados de miscota.pt colectados. Duração total: ', strftime("%M:%S", gmtime(elapsed)), 'minutos.')
    return

def getMiscotaEsPrice():
    start_time = time.time()
    print('\n>A coletar dados de miscota.es..')
    for link in miscotaEsLinks:
        siteLink = link[0]
        option = link[1]
        soup = get_data(siteLink)
        parse(soup, siteLink, option)
    xlsxMiscotaEs()
    elapsed = time.time() - start_time
    print('\n>Dados de miscota.es colectados. Duração total: ', strftime("%M:%S", gmtime(elapsed)), 'minutos.')
    return

def run():
    getMiscotaPtPrice()
    getMiscotaEsPrice()


# Escrever nos CSV's
def csvMiscotaPt():
    file = open('miscotaPT.csv', 'w', newline='')

    with file:
        # identifying header
        header = ['name', 'price', 'quantity', 'sku', 'link']
        writer = csv.DictWriter(file, fieldnames=header)

        writer.writeheader()
        for item in miscotaPrices:
            writer.writerow(item)
    miscotaPrices.clear()
    return

def csvMiscotaEs():
    file = open('miscotaES.csv', 'w', newline='')

    with file:
        # identifying header
        header = ['name', 'price', 'quantity', 'sku', 'link']
        writer = csv.DictWriter(file, fieldnames=header)

        writer.writeheader()
        for item in miscotaPrices:
            writer.writerow(item)
    miscotaPrices.clear()
    return

def xlsxMiscotaPt():
    pd.DataFrame(miscotaPrices).to_excel('miscotaPT.xlsx', header=True, index=False)
    miscotaPrices.clear()
    return


def xlsxMiscotaEs():
    pd.DataFrame(miscotaPrices).to_excel('miscotaES.xlsx', header=True, index=False)
    miscotaPrices.clear()
    return

"""
soup = get_data(url)
parse(soup, url)
"""

if __name__ == '__main__':
    getMiscotaPtPrice()
    getMiscotaEsPrice()

