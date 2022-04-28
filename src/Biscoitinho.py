import requests
from bs4 import BeautifulSoup
from selenium import webdriver
import csv
import pandas as pd
import time
from time import gmtime
from time import strftime

""" 
    TODO não permite pesquisar quantidades, vai sempre buscar a maior(igual à zooshop)
"""

#driver = webdriver.Firefox()

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36'
}


url = 'https://www.biscoitinho.pt/prod/acana/2321-acana-heritage-sport-e-agility.html'
url2 = 'https://www.biscoitinho.pt/prod/acana/2237-acana-singles-yorkshire-pork.html'
url3 = 'https://www.biscoitinho.pt/prod/acana/2749-acana-classics-prairie-poultry.html#/65-peso-11_4kg'
url4 = 'https://www.biscoitinho.pt/prod/acana/2749-acana-classics-prairie-poultry.html#/64-peso-17kg'

"""
o cehecked value não funciona em alguns dos links, está marcado um diferente do que o link indica
hardcoded o valor que deve procurar, necessário mais tarde procurar optimizar código
17kgs - 64
11.4  - 65

"""
biscoitinhoLinks = [
    ['https://www.biscoitinho.pt/prod/acana/2749-acana-classics-prairie-poultry.html#/65-peso-11_4kg','11,4kg'],
    ['https://www.biscoitinho.pt/prod/acana/2749-acana-classics-prairie-poultry.html#/64-peso-17kg','17kg'],
    ['https://www.biscoitinho.pt/prod/acana/2752-acana-classics-wild-coast.html#/65-peso-11_4kg','11,4kg'],
    ['https://www.biscoitinho.pt/prod/acana/2752-acana-classics-wild-coast.html#/64-peso-17kg','17kg'],
    ['https://www.biscoitinho.pt/prod/orijen/8-orijen-6-fish-dog.html','11,4kg'],
    ['https://www.biscoitinho.pt/prod/orijen/16-orijen-cat-kitten-tambem-para-furoes.html','5,4kg'],
    ]


biscoitinhoPrices = []

def get_data(url, driver):
    driver.get(url)
    time.sleep(4)
    html = driver.execute_script("return document.documentElement.outerHTML")
    sel_soup = BeautifulSoup(html, 'html.parser')
    return sel_soup


def parse(soup, url, value, driver):

    name = soup.find('h1', {'class': 'product_name'}).text.strip()

    biscoitinhoProduct = {
        'name': name,
        'price': soup.find('span', {'id': 'our_price_display'}).text.strip(),
        'quantity': value,
        'link': url,
    }
    biscoitinhoPrices.append(biscoitinhoProduct)


def getBiscoitinhoPrices(driver):
    start_time = time.time()
    print('\n>A coletar dados de biscoitinho.pt...')
    for link in biscoitinhoLinks:
        siteLink = link[0]
        value = link[1]
        sel_soup = get_data(siteLink, driver)
        parse(sel_soup, siteLink, value, driver)
    driver.close()
    print('>Dados de biscoitinho.pt colectados.\n')
    elapsed = time.time() - start_time
    print('\n>Dados de biscoitinho.pt colectados. Duração total: ', strftime("%M:%S", gmtime(elapsed)), 'minutos.')
    return

# para correr do program
def run():
    driver = webdriver.Firefox()
    getBiscoitinhoPrices(driver)
    xlsxBiscoitinho()

def csvBiscoitinho():
    file = open('biscoitinho.csv', 'w', newline='')

    with file:
        # identifying header
        header = ['name', 'price', 'reference', 'link']
        writer = csv.DictWriter(file, fieldnames=header)

        writer.writeheader()
        for item in biscoitinhoPrices:
            writer.writerow(item)
    biscoitinhoPrices.clear()
    return

def xlsxBiscoitinho():
    pd.DataFrame(biscoitinhoPrices).to_excel('biscoitinho.xlsx', header=True, index=False)
    biscoitinhoPrices.clear()
    return

"""
soup = get_data(url4)
parse(soup, url4, '11,4kg')
driver.close()
"""

#programa principal
if __name__ == '__main__':
    driver = webdriver.Firefox()
    getBiscoitinhoPrices(driver)
    xlsxBiscoitinho()

