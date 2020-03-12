# -*- coding: utf-8 -*-
import requests
from bs4 import BeautifulSoup
import pandas as pd


def table_data_text(table):       
    rows = []
    trs = table.find_all('tr')
    headerow = [td.get_text(strip=True) for td in trs[0].find_all('th')] # header row
    if headerow: # if there is a header row include first
        rows.append(headerow)
        trs = trs[1:]
    for tr in trs: # for every table row
        rows.append([td.get_text(strip=True) for td in tr.find_all('td')]) # data row
    return rows


def get_info_fundos():
    url = 'https://infofundos.com.br/fundos'
    print('Capturando informações do site', url)
    r = requests.get(url)

    soup = BeautifulSoup(r.text)
    html_table = soup.find('table', { 'id' : 't01' })

    list_table = table_data_text(html_table)
    df = pd.DataFrame(list_table[1:], columns=list_table[0])
    
    return df
