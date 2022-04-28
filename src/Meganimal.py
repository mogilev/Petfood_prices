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

url = 'https://www.meganimal.pt/pt/produtos/acana-heritage-dog-adult-large-breed/?&id_produto=16056&an=1&cg=41&gm=2&tc=8'

"""
Colocar opções:
    0 - Necessário 11 e 17kgs
    1 - 17 kgs
    2 - 11 kgs
    3 -  6 kgs
    4 -  5,4 kgs
    5 -  4,5 kgs
"""

meganimalLinks = [
    ['https://www.meganimal.pt/pt/produtos/acana-classics-dog-prairie-poultry/?&id_produto=17123&an=1&cg=41&gm=2&tc=8',0],
    ['https://www.meganimal.pt/pt/produtos/acana-classics-dog-red/?&id_produto=17125&an=1&cg=41&gm=2&tc=8',1],
    ['https://www.meganimal.pt/pt/produtos/acana-heritage-dog-adult-small-breed/?&id_produto=16054&an=1&cg=41&gm=2&tc=9',3],
    ['https://www.meganimal.pt/pt/produtos/acana-heritage-dog-light-fit/?&id_produto=16058&an=1&cg=41&gm=2&tc=8',2],
    ['https://www.meganimal.pt/pt/produtos/acana-cat-wild-prairie-new-formula/?&id_produto=24221&an=2&cg=41&gm=2&tc=2',5],
    ['https://www.meganimal.pt/pt/produtos/orijen-cat-kitten/?&id_produto=16217&an=2&cg=41&gm=2&tc=2',4],
    ]

meganimalPrices = []

def get_data(url):
    r = requests.get(url, headers=headers)
    soup = BeautifulSoup(r.text, 'html.parser')
    return soup


def parse(soup, url, option):
    results = soup.find('div', {'class': 'produto_opcoes'}).find_all('label', {'class': 'radiobox lato_classe5'})
    eraser = "g"
    quantities = []
    for result in results:
        teste = result.text.replace(u'\xa0', u'').replace(u'|', u' ').strip()
        qty = teste.split(eraser, 1)[0] + 'g'
        erased = teste.split(eraser, 1)[-1]
        pricel = erased.split(" ")
        price = pricel[1]
        name = soup.find('h1', {'class': 'lato_classe3 lato_classe_bold'}).text.strip()

        meganimalProduct = {
            'name': name,
            'price': price,
            'qty': qty,
            'link': url,
        }
        quantities.append(meganimalProduct)
        #print(meganimalProduct)

    if option == 0:
        if not any(item['qty'] == '11,4 kg' for item in quantities):
            meganimalProduct = {
                'name': soup.find('h1', {'class': 'lato_classe3 lato_classe_bold'}).text.strip(),
                'price': 'sem stock - confirmar',
                'qty': '11.4 Kg',
                'link': url,
            }
            meganimalPrices.append(meganimalProduct)
        else:
            for item in quantities:
                if item['qty'] == '11,4 kg':
                    meganimalPrices.append(item)

        if not any(item['qty'] == '17 kg' for item in quantities):
            meganimalProduct = {
                'name': soup.find('h1', {'class': 'lato_classe3 lato_classe_bold'}).text.strip(),
                'price': 'sem stock - confirmar',
                'qty': '17 Kg',
                'link': url,
            }
            meganimalPrices.append(meganimalProduct)
        else:
            for item in quantities:
                if item['qty'] == '17 kg':
                    meganimalPrices.append(item)
    if option == 1:
        if not any(item['qty'] == '17 kg' for item in quantities):
            meganimalProduct = {
                'name': soup.find('h1', {'class': 'lato_classe3 lato_classe_bold'}).text.strip(),
                'price': 'sem stock - confirmar',
                'qty': '17 Kg',
                'link': url,
            }
            meganimalPrices.append(meganimalProduct)
        else:
            for item in quantities:
                if item['qty'] == '17 kg':
                    meganimalPrices.append(item)

    if option == 2:
        if not any(item['qty'] == '11,4 kg' for item in quantities):
            meganimalProduct = {
                'name': soup.find('h1', {'class': 'lato_classe3 lato_classe_bold'}).text.strip(),
                'price': 'sem stock - confirmar',
                'qty': '11 Kg',
                'link': url,
            }
            meganimalPrices.append(meganimalProduct)
        else:
            for item in quantities:
                if item['qty'] == '11,4 kg':
                    meganimalPrices.append(item)

    if option == 3:
        if not any(item['qty'] == '6 kg' for item in quantities):
            meganimalProduct = {
                'name': soup.find('h1', {'class': 'lato_classe3 lato_classe_bold'}).text.strip(),
                'price': 'sem stock - confirmar',
                'qty': '17 Kg',
                'link': url,
            }
            meganimalPrices.append(meganimalProduct)
        else:
            for item in quantities:
                if item['qty'] == '6 kg':
                    meganimalPrices.append(item)

    if option == 4:
        if not any(item['qty'] == '5,4 kg' for item in quantities):
            meganimalProduct = {
                'name': soup.find('h1', {'class': 'lato_classe3 lato_classe_bold'}).text.strip(),
                'price': 'sem stock - confirmar',
                'qty': '17 Kg',
                'link': url,
            }
            meganimalPrices.append(meganimalProduct)
        else:
            for item in quantities:
                if item['qty'] == '5,4 kg':
                    meganimalPrices.append(item)

    if option == 5:
        if not any(item['qty'] == '4,5 kg' for item in quantities):
            meganimalProduct = {
                'name': soup.find('h1', {'class': 'lato_classe3 lato_classe_bold'}).text.strip(),
                'price': 'sem stock - confirmar',
                'qty': '17 Kg',
                'link': url,
            }
            meganimalPrices.append(meganimalProduct)
        else:
            for item in quantities:
                if item['qty'] == '4,5 kg':
                    meganimalPrices.append(item)


def getMeganimalPrices():
    start_time = time.time()
    print('\n>A coletar dados de meganimal.pt..')
    for link in meganimalLinks:
        sellink = link[0]
        option = link[1]
        soup = get_data(sellink)
        parse(soup, sellink, option)
    elapsed = time.time() - start_time
    print('\n>Dados de meganimal.pt colectados. Duração total: ', strftime("%M:%S", gmtime(elapsed)), 'minutos.')
    return

def run():
    getMeganimalPrices()
    xlsxMeganimal()


def csvMeganimal():
    file = open('meganimal.csv', 'w', newline='')
    with file:
        # identifying header
        header = ['name', 'price', 'qty', 'link']
        writer = csv.DictWriter(file, fieldnames=header)
        writer.writeheader()
        for item in meganimalPrices:
            writer.writerow(item)
    meganimalPrices.clear()
    return

def xlsxMeganimal():
    pd.DataFrame(meganimalPrices).to_excel('meganimal.xlsx', header=True, index=False)
    meganimalPrices.clear()
    return

"""
soup = get_data(url)
parse(soup, url)

"""

if __name__ == '__main__':
    getMeganimalPrices()
    xlsxMeganimal()
