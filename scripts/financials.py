import json
import requests
import pandas as pd
import filings

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

def search_cik(ticker):
    ticker = ticker.upper()
    # subsetting
    data = cik_list[cik_list['ticker']==ticker]['cik']
    data = data.values[0]

    # cik number received from source excludes 0s that comes first. Since cik is a 10-digit number, concatenate 0s.
    zeros = 10 - len(str(data))
    data = ('0' * zeros) + str(data)
    return data

# Company filing data
def get_sec_data(cik_num):
    url = f'https://data.sec.gov/api/xbrl/companyfacts/CIK{cik_num}.json'
    data = request_data(url)
    
    return data

# Taxonomy and facts
def get_facts(data, taxonomy):
    facts_dict = {}
    us_gaap_taxonomy = data['facts']['us-gaap']
    for i in taxonomy:
        facts_dict[i] = list(us_gaap_taxonomy[i]['units'].values())[0] # [0] is for removing unnecessary outer square bracket.

    return facts_dict

def extract_numbers(facts, taxonomy):
    # list to store data
    numbers = []

    return numbers

# latest fact fata
def get_latest(data):
    return data[-1]

# Getting cik list
cik_list = get_cik()

# Getting data from SEC
cik_num = search_cik('AAPL')

# Getting list of submitted filings 
# filings.get_filings_list(cik_num)

# test for Apple Inc. 
financial_data = get_sec_data(cik_num)
taxonomy = list(financial_data['facts']['us-gaap'].keys())

# Getting financial data
facts = get_facts(financial_data, taxonomy)

# test for Revenue (NEEDS TO BE CHANGED AFTER)
revenue_taxonomy = 'RevenueFromContractWithCustomerExcludingAssessedTax'
revenues = extract_numbers(facts, revenue_taxonomy)
print(revenues)

latest_revenue = get_latest(revenues)
print(latest_revenue)