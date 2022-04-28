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


url = 'https://www.tiendanimal.pt/acana-prairie-poultry-racao-para-caes-frango-p-12842.html'
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

tiendanimalptLinks = [
    ['https://www.tiendanimal.pt/acana-prairie-poultry-racao-para-caes-frango-p-12842.html',0],
    ['https://www.tiendanimal.pt/acana-wild-coast-racao-para-caes-peixe-p-12843.html',0],
    ['https://www.tiendanimal.pt/acana-classic-racao-para-caes-cordeiro-p-12844.html',1],
    ['https://www.tiendanimal.pt/acana-puppy-junior-p-4377.html',1],
    ['https://www.tiendanimal.pt/acana-puppy-large-breed-p-4378.html',1],
    ['https://www.tiendanimal.pt/acana-adult-small-breed-racas-pequenas-p-2164.html',3],
    ['https://www.tiendanimal.pt/acana-adult-p-7358.html',1],
    ['https://www.tiendanimal.pt/acana-adult-large-breed-p-4371.html',1],
    ['https://www.tiendanimal.pt/acana-adult-light-p-4372.html',2],
    ['https://www.tiendanimal.pt/acana-senior-p-4380.html',2],
    ['https://www.tiendanimal.pt/acana-wild-prairie-p-4343.html',2],
    ['https://www.tiendanimal.pt/acana-pacifica-p-4344.html',2],
    ['https://www.tiendanimal.pt/acana-wild-prairie-holistico-para-gatos-p-4335.html',5],
    ['https://www.tiendanimal.pt/orijen-canine-adulto-alimentacao-natural-para-caes-p-4217.html',2],
    ['https://www.tiendanimal.pt/orijen-adulto-peixes-alimentacao-natural-para-caes-p-4220.html',2],
    ['https://www.tiendanimal.pt/orijen-frango-gatos-gatinhos-furoes-p-4222.html',4],
    ]

tiendanimalEsLinks = [
    ['https://www.tiendanimal.es/acana-prairie-poultry-pienso-para-perros-pollo-p-12842.html',0],
    ['https://www.tiendanimal.es/acana-wild-coast-pienso-para-perros-pescado-p-12843.html',0],
    ['https://www.tiendanimal.es/acana-classic-pienso-para-perros-cordero-p-12844.html',1],
    ['https://www.tiendanimal.es/pienso-para-perros-acana-puppy-junior-p-4377.html',1],
    ['https://www.tiendanimal.es/acana-puppy-large-breed-p-4378.html',1],
    ['https://www.tiendanimal.es/acana-adult-small-breed-pienso-para-perros-mini-p-2164.html',3],
    ['https://www.tiendanimal.es/acana-adult-p-7358.html',1],
    ['https://www.tiendanimal.es/pienso-para-perros-acana-adult-large-breed-p-4371.html',1],
    ['https://www.tiendanimal.es/pienso-para-perros-acana-adult-light-p-4372.html',2],
    ['https://www.tiendanimal.es/pienso-para-perros-acana-senior-p-4380.html',2],
    ['https://www.tiendanimal.es/acana-wild-prairie-para-perros-pollo-p-4343.html',2],
    ['https://www.tiendanimal.es/pienso-acana-pacifica-para-perros-pescado-p-4344.html',2],
    ['https://www.tiendanimal.es/acana-wild-prairie-holistico-para-gatos-p-4335.html',5],
    ['https://www.tiendanimal.es/orijen-canine-adulto-alimentacion-natural-para-perros-p-4217.html',2],
    ['https://www.tiendanimal.es/orijen-canine-adulto-pescados-alimentacion-natural-para-perros-p-4220.html',2],
    ['https://www.tiendanimal.es/orijen-pollo-para-gatos-gatitos-hurones-p-4222.html',4],
    ]

tiendaAnimalPrices = []

def get_data(url):
    r = requests.get(url, headers=headers)
    soup = BeautifulSoup(r.text, 'html.parser')
    return soup

def parse(soup, url, option):
    results = soup.find_all('div', {'class':'js-opcion product-atributte__item product-atributte__item--gift'})
    url=url

    quantities = []
    for result in results:
        tiendaProduct = {
            'name': result.find('input', {'name': 'option_selector'})['data-product_name'],
            'price': result.find('div', {'class': 'price mt1'}).text.replace('€','').replace('.',',').strip(),
            'qty': result.find('div', {'class': 'fs-13 bold lh-1'}).text.strip(),
            'link': url,
            }
        quantities.append(tiendaProduct)

    if not any(d['name'] == 'Acana Prairie Poultry ração para cães com frango' or d['name'] == 'Acana Wild Coast ração para cães com peixe' or d['name'] == 'Acana Prairie Poultry pienso para perros con pollo' or d['name'] == 'Acana Wild Coast pienso para perros con pescado' for d in quantities): # tb se pode usar opção 0

        #print('não contém prairie poultry ou wild coast') #
        if option == 1:
            if not any(item['qty'] == '17 kg' for item in quantities):
                tiendaProduct = {
                    'name': result.find('input', {'name': 'option_selector'})['data-product_name'],
                    'price': 'sem stock - confirmar',
                    'qty': '17 Kg',
                    'link': url,
                }
                tiendaAnimalPrices.append(tiendaProduct)
            else:
                for item in quantities:
                    if item['qty'] == '17 kg':
                        tiendaProduct = {
                            'name': item['name'],
                            'price': item['price'],
                            'qty': item['qty'],
                            'link': url,
                        }
                        tiendaAnimalPrices.append(tiendaProduct)

        if option == 2:
            if not any(item['qty'] == '11.4 kg' for item in quantities):
                tiendaProduct = {
                    'name': result.find('input', {'name': 'option_selector'})['data-product_name'],
                    'price': 'sem stock - confirmar',
                    'qty': '11 Kg',
                    'link': url,
                }
                tiendaAnimalPrices.append(tiendaProduct)
            else:
                for item in quantities:
                    if item['qty'] == '11.4 kg':
                        tiendaProduct = {
                            'name': item['name'],
                            'price': item['price'],
                            'qty': item['qty'].replace('.', ','),
                            'link': url,
                        }
                        tiendaAnimalPrices.append(tiendaProduct)
                #print(quantities)
        if option == 3:
            if not any(item['qty'] == '6 kg' for item in quantities):
                tiendaProduct = {
                    'name': result.find('input', {'name': 'option_selector'})['data-product_name'],
                    'price': 'sem stock - confirmar',
                    'qty': '17 Kg',
                    'link': url,
                }
                tiendaAnimalPrices.append(tiendaProduct)
            else:
                for item in quantities:
                    if item['qty'] == '6 kg':
                        tiendaProduct = {
                            'name': item['name'],
                            'price': item['price'],
                            'qty': item['qty'],
                            'link': url,
                        }
                        tiendaAnimalPrices.append(tiendaProduct)

        if option == 4:
            if not any(item['qty'] == '5.4 kg' for item in quantities):
                tiendaProduct = {
                    'name': result.find('input', {'name': 'option_selector'})['data-product_name'],
                    'price': 'sem stock - confirmar',
                    'qty': '5,4 Kg',
                    'link': url,
                }
                tiendaAnimalPrices.append(tiendaProduct)
            else:
                for item in quantities:
                    if item['qty'] == '5.4 kg':
                        tiendaProduct = {
                            'name': item['name'],
                            'price': item['price'],
                            'qty': item['qty'].replace('.', ','),
                            'link': url,
                        }
                        tiendaAnimalPrices.append(tiendaProduct)
        if option == 5:
            if not any(item['qty'] == '4.5 kg' for item in quantities):
                tiendaProduct = {
                    'name': result.find('input', {'name': 'option_selector'})['data-product_name'],
                    'price': 'sem stock - confirmar',
                    'qty': '4,5 Kg',
                    'link': url,
                }
                tiendaAnimalPrices.append(tiendaProduct)
            else:
                for item in quantities:
                    if item['qty'] == '4.5 kg':
                        tiendaProduct = {
                            'name': item['name'],
                            'price': item['price'],
                            'qty': item['qty'].replace('.', ','),
                            'link': url,
                        }
                        tiendaAnimalPrices.append(tiendaProduct)

    else:
        #print('Contém prairie Poultry ou wild coast e entrou aqui')
        if not any(item['qty'] == '11.4 kg' for item in quantities):
            tiendaProduct = {
                'name': result.find('input', {'name': 'option_selector'})['data-product_name'],
                'price': 'sem stock - confirmar',
                'qty': '11,4 Kg',
                'link': url,
            }
            tiendaAnimalPrices.append(tiendaProduct)
        else:
            for item in quantities:
                if item['qty'] == '11.4 kg':
                    tiendaProduct = {
                        'name': item['name'],
                        'price': item['price'],
                        'qty': item['qty'].replace('.', ','),
                        'link': url,
                    }
                    tiendaAnimalPrices.append(tiendaProduct)


        if not any(item['qty'] == '17 kg' for item in quantities):
            tiendaProduct = {
                'name': result.find('input', {'name': 'option_selector'})['data-product_name'],
                'price': 'sem stock - confirmar',
                'qty': '17 Kg',
                'link': url,
            }
            tiendaAnimalPrices.append(tiendaProduct)
        else:
            for item in quantities:
                if item['qty'] == '17 kg':
                    tiendaProduct = {
                        'name': item['name'],
                        'price': item['price'],
                        'qty': item['qty'],
                        'link': url,
                    }
                    tiendaAnimalPrices.append(tiendaProduct)
    return


def getTiendaAnimalPrice():
    start_time = time.time()
    print('\n>A coletar dados de tiendaAnimal.pt...')
    for link in tiendanimalptLinks:
        siteLink = link[0]
        option = link[1]
        soup = get_data(siteLink)
        parse(soup, siteLink, option)
    xlsxTiendaPT()
    elapsed = time.time() - start_time
    print('\n>Dados de tiendaAnimal.pt colectados. Duração total: ', strftime("%M:%S", gmtime(elapsed)), 'minutos.')
    return

def getTiendaAnimalEsPrice():
    start_time = time.time()
    print('\n>A coletar dados de tiendaAnimal.es...')
    for link in tiendanimalEsLinks:
        siteLink = link[0]
        option = link[1]
        soup = get_data(siteLink)
        parse(soup, siteLink, option)
    xlsxTiendaES()
    elapsed = time.time() - start_time
    print('\n>Dados de tiendaAnimal.es colectados. Duração total: ', strftime("%M:%S", gmtime(elapsed)), 'minutos.')
    return

def run():
    getTiendaAnimalPrice()
    getTiendaAnimalEsPrice()


# Escrever nos CSV's
def csvTiendaPT():
    file = open('tiendaAnimalPT.csv', 'w', newline='')

    with file:
        # identifying header
        header = ['name', 'price', 'qty', 'link']
        writer = csv.DictWriter(file, fieldnames=header)

        writer.writeheader()
        for item in tiendaAnimalPrices:
            writer.writerow(item)
    tiendaAnimalPrices.clear()
    return

def csvTiendaES():
    file = open('tiendaAnimalES.csv', 'w', newline='')

    with file:
        # identifying header
        header = ['name', 'price', 'qty', 'link']
        writer = csv.DictWriter(file, fieldnames=header)

        writer.writeheader()
        for item in tiendaAnimalPrices:
            writer.writerow(item)
    tiendaAnimalPrices.clear()
    return

def xlsxTiendaPT():
    pd.DataFrame(tiendaAnimalPrices).to_excel('tiendaAnimalPT.xlsx', header=True, index=False)
    tiendaAnimalPrices.clear()
    return

def xlsxTiendaES():
    pd.DataFrame(tiendaAnimalPrices).to_excel('tiendaAnimalES.xlsx', header=True, index=False)
    tiendaAnimalPrices.clear()
    return


#soup = get_data(url2)
#parse(soup, url2)

if __name__ == '__main__':
    getTiendaAnimalPrice()
    getTiendaAnimalEsPrice()

