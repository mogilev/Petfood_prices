import requests
from bs4 import BeautifulSoup
from selenium import webdriver
import csv
import pandas as pd
import time
from time import gmtime
from time import strftime


#driver = webdriver.Firefox()

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36'
}

url = 'https://goldpet.pt/racao-seca-para-cao-adulto/18729-acana-classics-prairie-poultry-cao-adulto.html#/992-quantidade-114kg'

goldpetPrices = []

goldpetLinks = [
    'https://goldpet.pt/racao-seca-para-cao-adulto/18729-acana-classics-prairie-poultry-cao-adulto.html#/992-quantidade-114kg',
    'https://goldpet.pt/racao-seca-para-cao-adulto/18729-acana-classics-prairie-poultry-cao-adulto.html#/994-quantidade-17kg',
    'https://goldpet.pt/racao-seca-para-cao-adulto/18732-acana-classics-wild-coast-cao-adulto.html#/992-quantidade-114kg',
    'https://goldpet.pt/racao-seca-para-cao-adulto/18732-acana-classics-wild-coast-cao-adulto.html#/994-quantidade-17kg',

    ]


def get_data(url, driver):
    #driver = webdriver.Firefox()
    driver.get(url)
    time.sleep(3)
    html = driver.execute_script("return document.documentElement.outerHTML")
    sel_soup = BeautifulSoup(html, 'html.parser')
    return sel_soup


def parse(soup, url):
    results = soup.find_all('div', {'class', 'primary_block row'})
    url=url
    for item in results:
        product = {
            'name': item.find('h1',{'itemprop':'name'}).text,
            #'disponibility': item.find('p', {'id':'product_condition'}).text.replace('\n','').replace(' ',''),
            'availability': item.find('p', {'id': 'product_condition'}).find('span').text,
            'price': item.find('span', {'id':'our_price_display'}).text.replace('€','').replace(u'\xa0', u'').strip(), #'price': int(item.find('span', {'itemprop':'price'}).text.replace('€','').replace(u'\xa0', u'').replace(',','').strip())
         #   'reference': item.find('span', {'class': 'editable'}).text,
            'reference': item.find('p', {'id': 'product_reference'}).find('span',{'class':'editable'}).text,
            'link': url,
    }
        #'quantity': item.find('select', {'class': 'custom-select'}).find('option', {'selected': 'selected'}).text,
        goldpetPrices.append(product)
    return

def getGoldpetPrices(driver):
    start_time = time.time()
    print('\n>A coletar dados de goldpet.pt...')
    for link in goldpetLinks:
        sel_soup = get_data(link, driver)
        parse(sel_soup, link)
    driver.close()
    elapsed = time.time() - start_time
    print('\n>Dados de goldpet.pt colectados. Duração total: ', strftime("%M:%S", gmtime(elapsed)), 'minutos.')
    return

def run():
    driver = webdriver.Firefox()
    getGoldpetPrices(driver)
    xlsxGoldpet()


def csvGoldpet():
    file = open('goldpet.csv', 'w', newline='')

    with file:
        # identifying header
        header = ['name', 'availability', 'price', 'reference', 'link']
        writer = csv.DictWriter(file, fieldnames=header)

        writer.writeheader()
        for item in goldpetPrices:
            writer.writerow(item)
    goldpetPrices.clear()
    return

def xlsxGoldpet():
    pd.DataFrame(goldpetPrices).to_excel('goldpet.xlsx', header=True, index=False)
    goldpetPrices.clear()


#get_data(url)
#parse(sel_soup, url)

#getGoldpetPrices()
#csvGoldpet()



if __name__ == '__main__':
    getGoldpetPrices()
    xlsxGoldpet()
