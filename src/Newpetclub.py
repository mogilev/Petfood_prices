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

url = 'https://www.newpetclub.pt/acana-cat-homestead-harvest-gato-adulto'

newPetClubLinks = [
    ['https://www.newpetclub.pt/Caes/racao-para-caes/racao-caes-marcas/racao-caes-acana/acana-classics-prairie-poultry',0],
    ['https://www.newpetclub.pt/Caes/racao-para-caes/racao-caes-marcas/racao-caes-acana/acana-classics-wild-coast',0],
    ['https://www.newpetclub.pt/Caes/racao-para-caes/racao-caes-marcas/racao-caes-acana/acana-classics-red',1],
    ['https://www.newpetclub.pt/Caes/racao-para-caes/racao-caes-marcas/racao-caes-acana/acana-heritage-puppy-junior',1],
    ]


newPetClubPrices = []

def get_data(url):
    r = requests.get(url, headers=headers)
    soup = BeautifulSoup(r.text, 'html.parser')
    return soup


def parse(soup, url, option):
    results = soup.find('div', {'class':'col-md-6 col-sm-6 col-sms-12 col-xs-12'}).find_all('div',{'class':'radio'})
    name = soup.find('div', {'class': 'product-name'}).text
    url = url
    i = 1
    eraser = 'g'
    quantities = []
    for result in results:
        #print('iteração ', i)
        i += 1
        #print(result, '\n\n')
        kg = result.find('label').text.replace('€', '').replace(u'\xa0', u'').replace(u'-\n', u'').replace(u' ', u'').strip()
        price = result.find('span', {'class': 'price-option'}).text.replace('€', '').replace(u'\xa0', u'').strip()
        kgs = kg.split(eraser,1)[0]
        kg = kgs+'g'
        product = {
            'name': name,
            'price': price,
            'qty': kg,
            'link': url,
        }
        quantities.append(product)
        #print(quantities)

    if option == 0:
        if not any(item['qty'] == '11.4 kg' or item['qty'] == '11,4kg' for item in quantities):
            product = {
                'name': name,
                'price': 'sem stock - confirmar',
                'qty': '11.4 Kg',
                'link': url,
            }
            newPetClubPrices.append(product)
        else:
            for item in quantities:
                if item['qty'] == '11.4 kg' or item['qty'] == '11,4kg':
                    newPetClubPrices.append(item)

        if not any(item['qty'] == '17 kg' or item['qty'] == '17kg' for item in quantities):
            product = {
                'name': name,
                'price': 'sem stock - confirmar',
                'qty': '17 Kg',
                'link': url,
            }
            newPetClubPrices.append(product)
        else:
            for item in quantities:
                if item['qty'] == '17 kg' or item['qty'] == '17kg':
                    newPetClubPrices.append(item)

    if option == 1:
        if not any(item['qty'] == '17 kg' or item['qty'] == '17kg' for item in quantities):
            product = {
                'name': name,
                'price': 'sem stock - confirmar',
                'qty': '17 Kg',
                'link': url,
            }
            newPetClubPrices.append(product)
        else:
            for item in quantities:
                if item['qty'] == '17 kg' or item['qty'] == '17kg':
                    newPetClubPrices.append(item)

    if option == 2:
        if not any(item['qty'] == '11,4 kg' or item['qty'] == '11,4kg'  for item in quantities):
            product = {
                'name': name,
                'price': 'sem stock - confirmar',
                'qty': '11 Kg',
                'link': url,
            }
            newPetClubPrices.append(product)
        else:
            for item in quantities:
                if item['qty'] == '11.4 kg' or item['qty'] == '11,4kg':
                    newPetClubPrices.append(item)

    if option == 3:
        if not any(item['qty'] == '6kg' for item in quantities):
            product = {
                'name': name,
                'price': 'sem stock - confirmar',
                'qty': '17 Kg',
                'link': url,
            }
            newPetClubPrices.append(product)
        else:
            for item in quantities:
                if item['qty'] == '6kg':
                    newPetClubPrices.append(item)

    if option == 4:
        if not any(item['qty'] == '5,4 kg' or item['qty'] == '5,4kg' for item in quantities):
            product = {
                'name': name,
                'price': 'sem stock - confirmar',
                'qty': '17 Kg',
                'link': url,
            }
            newPetClubPrices.append(product)
        else:
            for item in quantities:
                if item['qty'] == '5,4 kg' or item['qty'] == '5,4kg':
                    newPetClubPrices.append(item)

    if option == 5:
        if not any(item['qty'] == '4,5kg' for item in quantities):
            product = {
                'name': name, #result.find('input', {'name': 'option_selector'})['data-product_name'],
                'price': 'sem stock - confirmar',
                'qty': '17 Kg',
                'link': url,
            }
            newPetClubPrices.append(product)
        else:
            for item in quantities:
                if item['qty'] == '4,5kg':
                    newPetClubPrices.append(item)


def getNewpetclubPrices():
    start_time = time.time()
    print('\n>A coletar dados de newpetclub.pt...')
    for link in newPetClubLinks:
        sLink = link[0]
        option = link[1]
        soup = get_data(sLink)
        parse(soup, sLink, option)
    elapsed = time.time() - start_time
    print('\n>Dados de newpetclub.pt colectados. Duração total: ', strftime("%M:%S", gmtime(elapsed)), 'minutos.')
    return

def run():
    getNewpetclubPrices()
    xlsxNewPetClub()


def csvNewPetClub():
    file = open('newPetClub.csv', 'w', newline='')
    with file:
        # identifying header
        header = ['name', 'price', 'qty', 'link']
        writer = csv.DictWriter(file, fieldnames=header)
        writer.writeheader()
        for item in newPetClubPrices:
            writer.writerow(item)
    newPetClubPrices.clear()
    return


def xlsxNewPetClub():
    pd.DataFrame(newPetClubPrices).to_excel('newPetClub.xlsx', header=True, index=False)
    newPetClubPrices.clear()
    return


"""
soup = get_data(url)
parse(soup, url)
"""


if __name__ == '__main__':
    getNewpetclubPrices()
    xlsxNewPetClub()

