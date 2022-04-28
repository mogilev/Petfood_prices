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


url = 'https://petcity.pt/acana-junior/1818-5869-acana-heritage-puppy-small-breed-ach100-064992502355.html#/4794,embalagem,340gr'


petcityLinks = [
    'https://petcity.pt/acana-adulto/1821-5841-acana-prairie-poultry-acc200-064992560355.html#/4792,embalagem,114kg',
    'https://petcity.pt/acana-adulto/1821-5842-acana-prairie-poultry-acc200-064992560355.html#/4793,embalagem,17kg',
    'https://petcity.pt/acana-adulto/1822-5863-acana-wild-coast-acc205-064992562342.html#/4792,embalagem,114kg',
    'https://petcity.pt/acana-adulto/1822-5864-acana-wild-coast-acc205-064992562342.html#/4793,embalagem,17kg',
    'https://petcity.pt/acana-adulto/1820-5868-acana-classic-red-acc210-064992561345.html#/4793,embalagem,17kg',
    ]

petcityPrices = []

def get_data(url):
    r = requests.get(url, headers=headers)
    soup = BeautifulSoup(r.text, 'html.parser')
    return soup

def parse(soup, url):
    results = soup.find_all('div', {'class', 'product-right-column col-12 col-md-6'})
    #print(len(results))
    url=url
    for item in results:
        product = {
            'title': item.find('h1',{'class':'h2 product-name'}).text,
            'availability': item.find('span', {'class':'product-available'}).text.replace('\n','').replace(' ',''),
            'price': item.find('span', {'itemprop':'price'}).text.replace('€','').replace(u'\xa0', u'').strip(), #'price': int(item.find('span', {'itemprop':'price'}).text.replace('€','').replace(u'\xa0', u'').replace(',','').strip())
            'quantity': item.find('select', {'class': 'custom-select'}).find('option',{'selected':'selected' }).text,
            'link': url,
    }
        petcityPrices.append(product)
        #print(product)
    return


def getPetcityPrice():
    start_time = time.time()
    print('\n>A coletar dados de petcity.pt...')
    for link in petcityLinks:
        soup = get_data(link)
        parse(soup, link)
    elapsed = time.time() - start_time
    print('>Dados de petcity.pt colectados. Duração total: ', strftime("%M:%S", gmtime(elapsed)), 'minutos. ')
    return

def csvPetcity():
    file = open('petCityPrices.csv', 'w', newline='')

    with file:
        # identifying header
        header = ['title', 'availability', 'price', 'quantity', 'link']
        writer = csv.DictWriter(file, fieldnames=header)

        writer.writeheader()
        for item in petcityPrices:
            writer.writerow(item)
    print('petCityPrices.csv criado com sucesso.')
    return

def xlsxPetcity():
    pd.DataFrame(petcityPrices).to_excel('petcity.xlsx', header=True, index=False)

#getPetcityPrice()
#print(petcityPrices)

def run():
    getPetcityPrice()
    xlsxPetcity()


if __name__ == '__main__':
    getPetcityPrice()
    xlsxPetcity()
