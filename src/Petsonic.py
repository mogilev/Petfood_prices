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

url = 'https://www.petsonic.com/pienso-para-perros-acana-cachorro-razas-grandes.html'
url2 = 'https://www.petsonic.com/pienso-para-perros-acana-grasslands-cordero.html'

"""
Colocar opções:
    0 - Necessário 11 e 17kgs
    1 - 17 kgs
    2 - 11 kgs
    3 -  6 kgs
    4 -  5,4 kgs
    5 -  4,5 kgs
"""

petsonicLinks = [
    ['https://www.petsonic.com/pienso-para-perros-acana-prairie-poultry.html?idpa=9646#/617-peso-11_4_kg_',0],
    ['https://www.petsonic.com/pienso-para-perros-acana-wild-coast.html?idpa=9651#/617-peso-11_4_kg_',0],
    ['https://www.petsonic.com/pienso-para-perros-acana-clasic-red.html?idpa=9657',1],
    ['https://www.petsonic.com/pienso-para-perros-acana-cachorros-razas-medianas.html?idpa=1944',1],
    ]

petsonicPrices = []

def get_data(url):
    r = requests.get(url, headers=headers)
    soup = BeautifulSoup(r.text, 'html.parser')
    return soup


def parse(soup, url, option):
    results = soup.find('ul', {'class': 'attribute_radio_list pundaline-variations'}).find_all('label')
    name = soup.find('h1', {'class': 'product_main_name'}).text.strip()
    quantities = []
    for result in results:
        #print('name: ', name)
        #print(result)
        petsonicProduct = {
            'name': name,
            'price': result.find('span', {'class': 'price_comb'}).text.replace('€', '').replace('.', ',').strip(),
            'qty': result.find('span', {'class': 'radio_label'}).text.strip(),
            'link': url,
        }
        quantities.append(petsonicProduct)

    #option = 0 # TODO apagar

    if option == 0:
        if not any(item['qty'] == '11,4 Kg.' or item['qty'] == '11.4 Kg.' for item in quantities):
            petsonicProduct = {
                'name': name,
                'price': 'sem stock - confirmar',
                'qty': '11.4 Kg',
                'link': url,
            }
            petsonicPrices.append(petsonicProduct)
        else:
            for item in quantities:
                if item['qty'] == '11,4 Kg'or item['qty'] == '11.4 Kg.':
                    petsonicPrices.append(item)

        if not any(item['qty'] == '17 Kg' for item in quantities):
            petsonicProduct = {
                'name': name,
                'price': 'sem stock - confirmar',
                'qty': '17 Kg',
                'link': url,
            }
            petsonicPrices.append(petsonicProduct)
        else:
            for item in quantities:
                if item['qty'] == '17 Kg':
                    petsonicPrices.append(item)
    if option == 1:
        if not any(item['qty'] == '17 Kg' for item in quantities):
            petsonicProduct = {
                'name': name,
                'price': 'sem stock - confirmar',
                'qty': '17 Kg',
                'link': url,
            }
            petsonicPrices.append(petsonicProduct)
        else:
            for item in quantities:
                if item['qty'] == '17 Kg':
                    petsonicPrices.append(item)

    if option == 2:
        if not any(item['qty'] == '11,4 Kg.' or item['qty'] == '11.4 Kg.' for item in quantities):
            petsonicProduct = {
                'name': name,
                'price': 'sem stock - confirmar',
                'qty': '11 Kg',
                'link': url,
            }
            petsonicPrices.append(petsonicProduct)
        else:
            for item in quantities:
                if item['qty'] == '11,4 Kg.' or item['qty'] == '11.4 Kg.' :
                    petsonicPrices.append(item)

    if option == 3:
        if not any(item['qty'] == '6 Kg' for item in quantities):
            petsonicProduct = {
                'name': name,
                'price': 'sem stock - confirmar',
                'qty': '17 Kg',
                'link': url,
            }
            petsonicPrices.append(petsonicProduct)
        else:
            for item in quantities:
                if item['qty'] == '6 Kg':
                    petsonicPrices.append(item)

    if option == 4:
        if not any(item['qty'] == '5,4 Kg' or item['qty'] == '5.4 kg' for item in quantities):
            petsonicProduct = {
                'name': name, #result.find('input', {'name': 'option_selector'})['data-product_name'],
                'price': 'sem stock - confirmar',
                'qty': '17 Kg',
                'link': url,
            }
            petsonicPrices.append(petsonicProduct)
        else:
            for item in quantities:
                if item['qty'] == '5,4 Kg' or item['qty'] == '5.4 kg':
                    petsonicPrices.append(item)

    if option == 5:
        if not any(item['qty'] == '4,5 Kg' or item['qty'] == '4.5 Kg' for item in quantities):
            petsonicProduct = {
                'name': name,  #result.find('input', {'name': 'option_selector'})['data-product_name'],
                'price': 'sem stock - confirmar',
                'qty': '17 Kg',
                'link': url,
            }
            petsonicPrices.append(petsonicProduct)
        else:
            for item in quantities:
                if item['qty'] == '4,5 Kg' or item['qty'] == '4.5 Kg':
                    petsonicPrices.append(item)


def getPetsonicPrices():
    start_time = time.time()
    print('\n>A coletar dados de petsonic.com...')
    for link in petsonicLinks:
        sel_link = link[0]
        option = link[1]
        soup = get_data(sel_link)
        parse(soup, sel_link, option)
    elapsed = time.time() - start_time
    print('\n>Dados de petsonic.com colectados. Duração total: ', strftime("%M:%S", gmtime(elapsed)), 'minutos.')
    return

def run():
    getPetsonicPrices()
    xlsxPetsonic()


def csvPetsonic():
    start_time = time.time()
    file = open('petsonic.csv', 'w', newline='')
    with file:
        # identifying header
        header = ['name', 'price', 'qty', 'link']
        writer = csv.DictWriter(file, fieldnames=header)
        writer.writeheader()
        for item in petsonicPrices:
            writer.writerow(item)
    petsonicPrices.clear()
    return

def xlsxPetsonic():
    pd.DataFrame(petsonicPrices).to_excel('petsonic.xlsx', header=True, index=False)
    petsonicPrices.clear()
    return

#getPetsonicPrices()
#csvPetsonic()
"""
soup = get_data(url)
parse(soup, url)
"""

if __name__ == '__main__':
    getPetsonicPrices()
    xlsxPetsonic()

