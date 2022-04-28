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


url = 'https://petness.pt/caes/acana/p-181469'
url2 = 'https://www.tiendanimal.pt/acana-wild-coast-racao-para-caes-peixe-p-12843.html'

"""
Colocar opções:
    0 - Necessário 11 e 17kgs
    1 - 17 kgs
    2 - 11 kgs
    3 -  6 kgs
    4 -  5,4 kgs
    5 -  4,5 kgs
"""
petnessLinks = [
    ['https://petness.pt/caes/acana/p-181469',0],
    ['https://petness.pt/caes/acana/p-181468',0],
    ['https://petness.pt/caes/acana/p-181472',1],
    ['https://petness.pt/caes/acana/p-181464',1],
    ]


petnessPrices = []

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
        petnessProduct = {
            'name': name,
            'price': result.find('span', {'class': 'variation-price'}).text.replace('€','').strip(),
            'qty': result.find('span', {'class': 'variation-name'}).text.strip(),
            'sku': result.find('meta', {'itemprop': 'sku'})['content'],
            'link': url,
            }
        quantities.append(petnessProduct)

    if option == 0:

        if not any(item['qty'] == '11,4 Kg' for item in quantities):
            petnessProduct = {
                'name': name,
                'price': 'não encontrado -verificar link',
                'qty': '11,4 Kg',
                'sku': 'não identificado',
                'link': url,
            }
            petnessPrices.append(petnessProduct)
        else:
            for item in quantities:
                if item['qty'] == '11,4 Kg':
                    petnessPrices.append(item)

        if not any(item['qty'] == '17 Kg' or item['qty'] == '17 kg' or item['qty'] == '17 KG' for item in quantities):
            petnessProduct = {
                'name': name,
                'price': 'não encontrado -verificar link',
                'qty': '17 Kg',
                'sku': 'não identificado',
                'link': url,
            }
            petnessPrices.append(petnessProduct)
        else:
            for item in quantities:
                if item['qty'] == '17 Kg':
                    petnessPrices.append(item)

    if option == 1:

        if not any(item['qty'] == '17 Kg' or item['qty'] == '17 kg' or item['qty'] == '17 KG' for item in quantities):
            petnessProduct = {
                'name': name,
                'price': 'não encontrado -verificar link',
                'qty': '17 Kg',
                'sku': 'não identificado',
                'link': url,
            }
            petnessPrices.append(petnessProduct)
        else:
            for item in quantities:
                if item['qty'] == '17 Kg' or item['qty'] == '17 kg' or item['qty'] == '17 KG':
                    petnessPrices.append(item)


    if option == 2:

        if not any(item['qty'] == '11,4 Kg' or item['qty'] == '11,4 kg' for item in quantities):
            petnessProduct = {
                'name': name,
                'price': 'não encontrado -verificar link',
                'qty': '11,4 Kg',
                'sku': 'não identificado',
                'link': url,
            }
            petnessPrices.append(petnessProduct)
        else:
            for item in quantities:
                if item['qty'] == '11,4 Kg' or item['qty'] == '11,4 kg':
                    petnessPrices.append(item)

    if option == 3:

        if not any(item['qty'] == '6 Kg' for item in quantities):
            petnessProduct = {
                'name': name,
                'price': 'não encontrado -verificar link',
                'qty': '11,4 Kg',
                'sku': 'não identificado',
                'link': url,
            }
            petnessPrices.append(petnessProduct)
        else:
            for item in quantities:
                if item['qty'] == '6 Kg':
                    petnessPrices.append(item)


    if option == 4:
        if not any(item['qty'] == '5,4 Kg' or item['qty'] == '5,4 KG' for item in quantities):
            petnessProduct = {
                'name': name,
                'price': 'não encontrado -verificar link',
                'qty': '5,4 KG',
                'sku': 'não identificado',
                'link': url,
            }
            petnessPrices.append(petnessProduct)
        else:
            for item in quantities:
                if item['qty'] == '5,4 Kg' or item['qty'] == '5,4 KG':
                    petnessPrices.append(item)


    if option == 5:
        if not any(item['qty'] == '4,5 Kg' or item['qty'] == '4,5 KG' for item in quantities):
            petnessProduct = {
                'name': item['name'],
                'price': item['price'],
                'qty': item['quantity'],
                'sku': item['sku'],
                'link': item['link'],
            }
            petnessPrices.append(petnessProduct)
        else:
            for item in quantities:
                if item['qty'] == '4,5 Kg' or item['qty'] == '4,5 KG':
                    petnessPrices.append(item)


def getPetnessPrice():
    start_time = time.time()
    print('\n>A coletar dados de petness.pt...')
    for link in petnessLinks:
        siteLink = link[0]
        option = link[1]
        soup = get_data(siteLink)
        parse(soup, siteLink, option)
    elapsed = time.time() - start_time
    print('\n>Dados de petness.pt colectados. Duração total: ', strftime("%M:%S", gmtime(elapsed)), 'minutos.')
    return

def run():
    getPetnessPrice()
    xlsxPetness()


# Escrever nos CSV's
def csvPetness():
    file = open('petness.csv', 'w', newline='')

    with file:
        # identifying header
        header = ['name', 'price', 'qty', 'sku', 'link']
        writer = csv.DictWriter(file, fieldnames=header)

        writer.writeheader()
        for item in petnessPrices:
            writer.writerow(item)
    petnessPrices.clear()
    return

def xlsxPetness():
    pd.DataFrame(petnessPrices).to_excel('petness.xlsx', header=True, index=False)
    petnessPrices.clear()
    return


"""
soup = get_data(url)
parse(soup, url)
"""

if __name__ == '__main__':
    getPetnessPrice()
    xlsxPetness()

