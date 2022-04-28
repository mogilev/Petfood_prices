import requests
from bs4 import BeautifulSoup
from selenium import webdriver
import csv
import time
import pandas as pd
import time
from time import gmtime
from time import strftime

#driver = webdriver.Firefox()

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36'
}


url = 'https://www.zooshop.pt/prod/acana/2311-acana-heritage-puppy-large-breed.html'
url2 = 'https://www.biscoitinho.pt/prod/acana/2237-acana-singles-yorkshire-pork.html'

zooshopLinks = [
    ['https://www.zooshop.pt/prod/acana/2749-acana-classics-prairie-poultry.html#/65-peso-11_4kg','11,4kg'],
    ['https://www.zooshop.pt/prod/acana/2749-acana-classics-prairie-poultry.html#/64-peso-17kg','17kg'],
    ['https://www.zooshop.pt/prod/acana/2752-acana-classics-wild-coast.html#/65-peso-11_4kg','11,4kg'],
    ['https://www.zooshop.pt/prod/acana/2752-acana-classics-wild-coast.html#/64-peso-17kg','17kg'],
    ['https://www.zooshop.pt/prod/acana/2755-acana-classics-classic-red.html#/64-peso-17kg','17kg'],
    ['https://www.zooshop.pt/prod/acana/2310-acana-heritage-puppy-e-junior.html#/64-peso-17kg', '17kg'],
    ['https://www.zooshop.pt/prod/acana/2311-acana-heritage-puppy-large-breed.html#/64-peso-17kg', '17kg'],
    ['https://www.zooshop.pt/prod/acana/2314-acana-heritage-adult-small-breed.html#/102-peso-6kg','6kg'],
    ['https://www.zooshop.pt/prod/acana/2316-acana-heritage-adult-dog.html#/64-peso-17kg','17kg'],
    ['https://www.zooshop.pt/prod/acana/2319-acana-heritage-adult-large-breed.html#/64-peso-17kg','17kg'],
    ['https://www.zooshop.pt/prod/acana/3353-acana-heritage-light-e-fit.html#/65-peso-11_4kg','11,4kg'],
    ['https://www.zooshop.pt/prod/acana/3352-acana-heritage-senior-dog.html#/65-peso-11_4kg','11,4kg'],
    ['https://www.zooshop.pt/prod/acana/20-acana-regionals-sem-cereais-wild-prairie-dog.html#/65-peso-11_4kg','11,4kg'],
    ['https://www.zooshop.pt/prod/acana/22-acana-regionals-sem-cereais-pacifica-dog.html#/65-peso-11_4kg','11,4kg'],
    ['https://www.zooshop.pt/prod/acana/29-acana-regionals-sem-cereais-wild-prairie-cat-e-kitten.html#/170-peso-4_5kg','4,5kg'],
    ['https://www.zooshop.pt/prod/orijen/1581-orijen-original-dog.html#/65-peso-11_4kg','11,4kg'],
    ['https://www.zooshop.pt/prod/orijen/8-orijen-6-fish-dog.html#/65-peso-11_4kg','11,4kg'],
    ['https://www.zooshop.pt/prod/orijen/16-orijen-cat-kitten-tambem-para-furoes.html','5,4kg'],
    ]

zooshopPrices = []

def get_data(url, driver):
    driver.get(url)
    time.sleep(4)
    html = driver.execute_script("return document.documentElement.outerHTML")
    sel_soup = BeautifulSoup(html, 'html.parser')
    return sel_soup


def parse(soup, url, value):

    #name = soup.find('h1', {'class': 'product_name'}).text.strip()
    name = soup.find('title').text.strip()
    zooshopProduct = {
        'name': name,
        'price': soup.find('span', {'id': 'our_price_display'}).text.strip(),
        'quantity': value,
        'link': url,
    }
    zooshopPrices.append(zooshopProduct)

    """
    name = soup.find('title').text.strip()
    correctValue = soup.find('input', {'checked': 'checked'})['value']
    results = soup.find_all('form', {'id':'buy_block'})
    url=url
    kg = ""

    weightResultsKG = soup.find('div',{'class': 'attribute_list'}).find_all('li')

    for i in weightResultsKG:
        spans = i.find_all('span')
        checker = spans[0].find('input', {'class': 'attribute_radio'})['value']
        if checker == correctValue:
            kg = spans[1].text

    for result in results:
        zooshopProduct = {
            'name': name,
            'price': result.find('span', {'id': 'our_price_display'})['content'],
            'quantity': kg,
            'link': url,
        }
        print(zooshopProduct)
        zooshopPrices.append(zooshopProduct)
    """

def getZooshopPrices(driver):
    start_time = time.time()
    print('\n>A coletar dados de zooshop...')
    for link in zooshopLinks:
        siteLink = link[0]
        value = link[1]
        sel_soup = get_data(siteLink, driver)
        parse(sel_soup, siteLink, value)
    driver.close()
    elapsed = time.time() - start_time
    print('\n>Dados de zooshop colectados. Duração total: ', strftime("%M:%S", gmtime(elapsed)), 'minutos.')
    return


def run():
    driver = webdriver.Firefox()
    getZooshopPrices(driver)
    xlsxZooshop()

def csvZooshop():
    file = open('zooshop.csv', 'w', newline='')

    with file:
        # identifying header
        header = ['name', 'price', 'reference', 'link']
        writer = csv.DictWriter(file, fieldnames=header)

        writer.writeheader()
        for item in zooshopPrices:
            writer.writerow(item)
    zooshopPrices.clear()
    return

def xlsxZooshop():
    pd.DataFrame(zooshopPrices).to_excel('zooshop.xlsx', header=True, index=False)
    zooshopPrices.clear()
    return


"""
soup = get_data(url)
parse(soup, url, '17kg')
"""

#programa principal
if __name__ == '__main__':
    getZooshopPrices()
    xlsxZooshop()


