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


url = 'https://www.kiwoko.pt/caes/comida-para-caes/racao-seca-para-caes/alimentacao-natural/acana-adult-racao-para-cao/ACAACB02_M.html'


"""
Colocar opções:
    0 - Necessário 11 e 17kgs
    1 - 17 kgs
    2 - 11 kgs
    3 -  6 kgs
    4 -  5,4 kgs
    5 -  4,5 kgs
"""

kiwokoLinksPT = [
    ['https://www.kiwoko.pt/caes/comida-para-caes/racao-seca-para-caes/acana-prairie-poultry/ACACAP17_M.html',0],
    ['https://www.kiwoko.pt/caes/comida-para-caes/racao-seca-para-caes/acana-wild-coast/ACACAW11_M.html',0],
    ['https://www.kiwoko.pt/alimentacion-perro/acana-classic-red-pienso-para-perros-con-cordero/ACACAR11.html',1],
    ['https://www.kiwoko.pt/caes/comida-para-caes/racao-seca-para-caes/alimentacao-natural/acana-small-breed-adult-racao-para-cao/ACAAAS02_M.html',3],
    ['https://www.kiwoko.pt/gatos/comida-para-gatos/racao-para-gatos/acana-feline-wild-prairie/ACAAWC02_M.html',5],
    ['https://www.kiwoko.pt/gatos/comida-para-gatos/racao-para-gatos/orijen-feline-cat_kitten/ORJOC07_M.html',4],
    ]

kiwokoLinksES = [
    ['https://www.kiwoko.com/perros/comida-para-perros/pienso-seco-para-perros/pienso-natural/acana-prairie-poultry-pienso-para-perros-con-pollo/ACACAP17_M.html',0],
    ['https://www.kiwoko.com/perros/comida-para-perros/pienso-seco-para-perros/pienso-natural/acana-classic-red-pienso-para-perros-con-cordero/ACACAR11_M.html',1],
    ['https://www.kiwoko.com/perros/comida-para-perros/pienso-seco-para-perros/pienso-natural/acana-adult-small-breed-pienso-para-perros/ACAAAS02_M.html',3],
    ['https://www.kiwoko.com/perros/comida-para-perros/pienso-seco-para-perros/pienso-natural/acana-adult-dog/ACAACB02_M.html',1],
    ['https://www.kiwoko.com/perros/comida-para-perros/pienso-seco-para-perros/pienso-natural/acana-adult-light_fit/ACAALF13_M.html',2],
    ['https://www.kiwoko.com/gatos/comida-para-gatos/pienso-seco-para-gatos/acana-feline-wild-prairie/ACAAWC02_M.html',5],
    ['https://www.kiwoko.com/perros/comida-para-perros/pienso-seco-para-perros/pienso-natural/pienso-para-perros-orijen-adult/ORJOA02_M.html',2],
    ['https://www.kiwoko.com/gatos/comida-para-gatos/pienso-seco-para-gatos/orijen-feline-cat_kitten/ORJOC07_M.html',4],
    ]

kiwokoPrices = []


def get_data(url, driver):
    driver.get(url)
    time.sleep(4)
    html = driver.execute_script("return document.documentElement.outerHTML")
    sel_soup = BeautifulSoup(html, 'html.parser')
    return sel_soup

def parse(soup, url, option):
    header = soup.find('h1', {'class': 'product-name heading-title text-uppercase'}).text
    results = soup.find_all('div', {'class': 'custom-radio-group'})
    url = url
    quantities = []
    for item in results:
        preco = item.find('li', {'class': 'sales'})
        if item.find('li', {'class': 'sales'}) is not None:
            preco = item.find('li', {'class': 'sales'}).text.replace('€', '').replace(u'\xa0', u'').strip()
        product = {
            'name': header,
            'price': preco,
            'qty': item.find('label', {'for': 'attrValue'}).text.replace('.', ','),
            'link': url,
        }
        quantities.append(product)

    if option == 0:
        if not any(item['qty'] == '11.4kg' or item['qty'] == '11kg' or item['qty'] == '11,4kg' or item['qty'] == '11,4 kg' or item['qty'] == '11.4 kg' for item in quantities):
            kiwokoProduct = {
                'name': header,
                'price': 'sem stock - confirmar',
                'qty': '11,4 Kg',
                'link': url,
            }
            kiwokoPrices.append(kiwokoProduct)
        else:
            for item in quantities:
                if item['qty'] == '11.4kg' or item['qty'] == '11kg' or item['qty'] == '11,4kg' or item['qty'] == '11,4 kg' or item['qty'] == '11.4 kg':
                    kiwokoPrices.append(item)

        if not any(item['qty'] == '17kg' or item['qty'] == '17 kg' for item in quantities):
            kiwokoProduct = {
                'name': header,
                'price': 'sem stock - confirmar',
                'qty': '17 Kg',
                'link': url,
            }
            kiwokoPrices.append(kiwokoProduct)
        else:
            for item in quantities:
                if item['qty'] == '17kg' or item['qty'] == '17 kg':
                    kiwokoPrices.append(item)

    if option == 1:
        if not any(item['qty'] == '17kg' or item['qty'] == '17 kg' for item in quantities):
            kiwokoProduct = {
                'name': header,
                'price': 'sem stock - confirmar',
                'qty': '17 Kg',
                'link': url,
            }
            kiwokoPrices.append(kiwokoProduct)
        else:
            for item in quantities:
                if item['qty'] == '17kg' or item['qty'] == '17 kg':
                    kiwokoPrices.append(item)

    if option == 2:
        if not any(item['qty'] == '11.4kg' or item['qty'] == '11kg' or item['qty'] == '11,4kg' or item['qty'] == '11,4 kg' or item['qty'] == '11.4 kg' for item in quantities):
            kiwokoProduct = {
                'name': header,
                'price': 'sem stock - confirmar',
                'qty': '11,4 Kg',
                'link': url,
            }
            kiwokoPrices.append(kiwokoProduct)
        else:
            for item in quantities:
                if item['qty'] == '11.4kg' or item['qty'] == '11kg' or item['qty'] == '11,4kg' or item['qty'] == '11,4 kg' or item['qty'] == '11.4 kg':
                    kiwokoPrices.append(item)

    if option == 3:
        if not any(item['qty'] == '6kg' for item in quantities):
            kiwokoProduct = {
                'name': header,
                'price': 'sem stock - confirmar',
                'qty': '6 Kg',
                'link': url,
            }
            kiwokoPrices.append(kiwokoProduct)
        else:
            for item in quantities:
                if item['qty'] == '6kg':
                    kiwokoPrices.append(item)

    if option == 4:
        if not any(item['qty'] == '5,4kg' for item in quantities):
            kiwokoProduct = {
                'name': header,
                'price': 'sem stock - confirmar',
                'qty': '5,4 Kg',
                'link': url,
            }
            kiwokoPrices.append(kiwokoProduct)
        else:
            for item in quantities:
                if item['qty'] == '5,4kg':
                    kiwokoPrices.append(item)

    if option == 5:
        if not any(item['qty'] == '4,5kg' for item in quantities):
            kiwokoProduct = {
                'name': header,
                'price': 'sem stock - confirmar',
                'qty': '4,5 Kg',
                'link': url,
            }
            kiwokoPrices.append(kiwokoProduct)
        else:
            for item in quantities:
                if item['qty'] == '4,5kg':
                    item['qty'].replace('.', ',')
                    kiwokoPrices.append(item)
                    #print(kiwokoProduct)  # print de teste
    return


def getKiwokoPtPrice(driver):
    start_time = time.time()
    print('\n>A coletar dados de kiwoko.pt...')
    for link in kiwokoLinksPT:
        siteLink = link[0]
        option = link[1]
        sel_soup = get_data(siteLink, driver)
        parse(sel_soup, siteLink, option)
    xlsxKiwokoPt()
    elapsed = time.time() - start_time
    print('\n>Dados de kiwoko.pt colectados. Duração total: ', strftime("%M:%S", gmtime(elapsed)), 'minutos.')
    return

def getKiwokoEsPrice(driver):
    start_time = time.time()
    print('\n>A coletar dados de kiwoko.com...')
    for link in kiwokoLinksES:
        siteLink = link[0]
        option = link[1]
        sel_soup = get_data(siteLink, driver)
        parse(sel_soup, siteLink, option)
    driver.close()
    xlsxKiwokoEs()
    elapsed = time.time() - start_time
    print('\n>Dados de kiwoko.com colectados. Duração total: ', strftime("%M:%S", gmtime(elapsed)), 'minutos.')
    return

def run():
    driver = webdriver.Firefox()
    getKiwokoPtPrice(driver)
    getKiwokoEsPrice(driver)


# Escrever nos CSV's
def csvKiwokoPT():
    file = open('KiwokoPT.csv', 'w', newline='')

    with file:
        # identifying header
        header = ['name', 'price', 'qty', 'link']
        writer = csv.DictWriter(file, fieldnames=header)

        writer.writeheader()
        for item in kiwokoPrices:
            writer.writerow(item)
    kiwokoPrices.clear()
    return

def csvKiwokoES():
    file = open('KiwokoES.csv', 'w', newline='')

    with file:
        # identifying header
        header = ['name', 'price', 'qty', 'link']
        writer = csv.DictWriter(file, fieldnames=header)

        writer.writeheader()
        for item in kiwokoPrices:
            writer.writerow(item)
    kiwokoPrices.clear()
    return

def xlsxKiwokoPt():
    pd.DataFrame(kiwokoPrices).to_excel('KiwokoPT.xlsx', header=True, index=False)
    kiwokoPrices.clear()

def xlsxKiwokoEs():
    pd.DataFrame(kiwokoPrices).to_excel('KiwokoES.xlsx', header=True, index=False)
    kiwokoPrices.clear()




if __name__ == '__main__':
    driver = webdriver.Firefox()
    getKiwokoPtPrice(driver)
    getKiwokoEsPrice(driver)



