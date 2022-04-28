import pandas as pd
import re

rootPath = "C:\\<path>\\<file>\\"

lastPath = "C:\\<path>\\<file>\\"


#sms = pd.read_csv("spam.csv", encoding="latin-1")

prices = pd.read_excel("C:\\<path>\\<file>")

#prices = prices.rename(columns={'name': 'Label', 'v2': 'Text'})

prices = prices[['name', 'quantity', 'price', 'link']]

print(prices)

prices = prices[['name', 'quantity', 'price']]

print(prices)

prices = prices.rename(columns={'price':'biscoitinho'})

print(prices)

amasc = pd.read_excel("C:\\<path>\\<file>")

prices.insert(3,'amascotadosPT', amasc['price'])

print(prices)