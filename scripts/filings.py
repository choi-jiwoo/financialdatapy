import json
import requests
import pandas as pd
from bs4 import BeautifulSoup
import re

# Request data from sec.gov
def request_data(url):
    headers = {'User-Agent' : 'Mozilla'}
    res = requests.get(url, headers=headers)
    data = json.loads(res.text)
    return data

# CIK
def get_cik():
    url = 'https://www.sec.gov/files/company_tickers_exchange.json'
    data = request_data(url)

    cik_list = pd.DataFrame(data['data'], columns=data['fields'])
    # uniform company names
    cik_list['name'] = cik_list['name'].str.lower().str.title()

    return cik_list

def search_cik(cik_list, ticker):
    ticker = ticker.upper()
    # subsetting
    data = cik_list[cik_list['ticker']==ticker]['cik']
    data = data.values[0]

    # cik number received from source excludes 0s that comes first. Since cik is a 10-digit number, concatenate 0s.
    zeros = 10 - len(str(data))
    data = ('0' * zeros) + str(data)
    return data

# Company filings list
def get_filings_list(cik): 
    url = f'http://data.sec.gov/submissions/CIK{cik}.json'
    data = request_data(url)

    acc = data['filings']['recent']['accessionNumber']
    acc = [s.replace('-', '') for s in acc]
    form = data['filings']['recent']['form']
    doc = data['filings']['recent']['primaryDocument']

    filings = pd.DataFrame(zip(form, acc, doc), columns=['AccessionNumber', 'Form', 'PrimaryDocument'])

    return filings

def get_link(cik, latest, file_list, pattern):
    regex = re.compile(pattern, flags=re.IGNORECASE)

    for i in file_list:
        if regex.search(i[0]):
            link = f'https://www.sec.gov/Archives/edgar/data/{cik}/{latest}/{i[1]}.htm'
            break
    return link

# only for the latest 10-K filing 
def get_latest_10K(cik, latest):
    url = f'https://www.sec.gov/cgi-bin/viewer?action=view&cik={cik}&accession_number={latest}&xbrl_type=v'
    res = request_data(url)
    soup = BeautifulSoup(res.text)

    menu = soup.find(id='menu')
    a = menu.find_next('a', string='Financial Statements')
    ul = a.find_next('ul')
    li = ul.find_all('li')

    # element names in financial statements
    element = [x.get_text() for x in li]
    # filenames of each 3 statements
    filename = [re.search('r\d', str(x)).group().upper() for x in li]
    file_list = list(zip(element, filename))

    # get link for each financial statement
    unmatch = '(?!\(parenthetical+s?\))([a-z0-9]+)$'
    # income statement
    is_pattern = '(((?<!comprehensive)\sincome)|operation+s?|earning+s?)'+ unmatch
    is_l = get_link(cik, latest, file_list, is_pattern)

    # balance sheet
    bs_pattern = '(balance\ssheet+s?)'+ unmatch
    bs_l = get_link(cik, latest, file_list, bs_pattern)

    # cash flow
    cf_pattern = '(cash\sflow+s?)'+ unmatch
    cf_l = get_link(cik, latest, file_list, cf_pattern)

    financial_statement_link = dict({'income_statement' : is_l,
                                     'balance_sheet' : bs_l,
                                     'cash_flow' : cf_l})

    return financial_statement_link