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



url = 'https://www.amascotados.pt/acana/2906-ruched-prairie-poultry-114-kg-0064992560119.html'
url2 = 'https://www.amascotados.pt/acana/2889-ruched-prairie-poultry-17-kg-0064992560171.html'

amascotadosPtLinks = [
    'https://www.amascotados.pt/acana/2906-ruched-prairie-poultry-114-kg-0064992560119.html',
    'https://www.amascotados.pt/acana/2889-ruched-prairie-poultry-17-kg-0064992560171.html',
    'https://www.amascotados.pt/acana/3097-ruched-wild-coast-114-kg-0064992562120.html',
    'https://www.amascotados.pt/acana/3098-ruched-wild-coast-17-kg-0064992562175.html',
    'https://www.amascotados.pt/acana/2601-ruched-puppy-junior-17-kg-064992500177.html',
    'https://www.amascotados.pt/acana/2615-ruched-puppy-large-breed-17-kg-064992501174.html',
    'https://www.amascotados.pt/orijen/2275-orijen-cat-gatinho-68-kg-064992280543.html',
    ]

amascotadosEsLinks = [
    'https://www.amascotados.com/acana/2906-acana-prairie-poultry-114-kg-0064992560119.html',
    'https://www.amascotados.com/acana/2889-acana-praire-poultry-17-kg-0064992560171.html',
    'https://www.amascotados.com/acana/3097-acana-wild-coast-114-kg-0064992562120.html',
    'https://www.amascotados.com/acana/3098-acana-wild-coast-114-kg-0064992562175.html',
    'https://www.amascotados.com/acana/2601-acana-puppy-junior-18-kg-064992500177.html',
    'https://www.amascotados.com/orijen/2160-orijen-6-fish-for-dog-13-kg-064992183127.html',
    'https://www.amascotados.com/orijen/2275-orijen-cat-amp-kitten-6-8-kg-064992280543.html',
    ]

amascotadosPrices = []


def get_data(url, driver):
    driver.get(url)
    time.sleep(2)
    html = driver.execute_script("return document.documentElement.outerHTML")
    sel_soup = BeautifulSoup(html, 'html.parser')
    return sel_soup


def parse(soup, url, driver):
    results = soup.find('span', {'id': 'our_price_display'}).text.replace('€', '').replace(u'\xa0', u'').strip()
    name = soup.find('img', {'id': 'bigpic'})['title']
    url = url
    availability = soup.find('span', {'id': 'availability_value'})['class']
    if availability[1] == "label-danger":
        availability = 'sem stock'
    else:
        availability = 'OK'
    amascotadosProduct = {
        'name': name,
        'availability': availability,
        'price': results,
        'link': url,
    }
    #print(amascotadosProduct)
    amascotadosPrices.append(amascotadosProduct)
    return


def getAmascotadosPtPrice(driver):
    start_time = time.time()
    #driver = webdriver.Firefox()
    print('\n>A coletar dados de amascotados.pt...')
    for link in amascotadosPtLinks:
        soup = get_data(link, driver)
        parse(soup, link, driver)
    xlsxAmascotadosPT()
    #driver.close()
    elapsed = time.time() - start_time
    print('\n>Dados de amascotados.pt colectados. Duração total: ', strftime("%M:%S", gmtime(elapsed)), 'minutos.')
    return

def getAmascotadosEsPrice(driver):
    start_time = time.time()
    print('\n>A coletar dados de amascotados.es...')
    for link in amascotadosEsLinks:
        soup = get_data(link, driver)
        parse(soup, link, driver)
    driver.close()
    xlsxAmascotadosES()
    elapsed = time.time() - start_time
    print('\n>Dados de amascotados.es colectados. Duração total: ', strftime("%M:%S", gmtime(elapsed)), 'minutos.')
    return

def run():
    driver = webdriver.Firefox()
    getAmascotadosPtPrice(driver)
    getAmascotadosEsPrice(driver)


def csvAmascotadosPT():
    file = open('amascotadosPT.csv', 'w', newline='')

    with file:
        # identifying header
        header = ['name', 'price', 'link']
        writer = csv.DictWriter(file, fieldnames=header)

        writer.writeheader()
        for item in amascotadosPrices:
            writer.writerow(item)
    return

def csvAmascotadosES():
    file = open('amascotadosES.csv', 'w', newline='')

    with file:
        # identifying header
        header = ['name', 'price', 'link']
        writer = csv.DictWriter(file, fieldnames=header)

        writer.writeheader()
        for item in amascotadosPrices:
            writer.writerow(item)
    return

def xlsxAmascotadosPT():
    pd.DataFrame(amascotadosPrices).to_excel('amascotadosPT.xlsx', header=True, index=False)
    amascotadosPrices.clear()
    return

def xlsxAmascotadosES():
    pd.DataFrame(amascotadosPrices).to_excel('amascotadosES.xlsx', header=True, index=False)
    amascotadosPrices.clear()
    return


"""
soup = get_data(url)
parse(soup, url)
"""

if __name__ == '__main__':
    driver = webdriver.Firefox()
    getAmascotadosPtPrice(driver)
    getAmascotadosEsPrice(driver)

