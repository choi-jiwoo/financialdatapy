import json
import requests
import re
import cik

# Getting cik list
def search_cik(ticker):
    # subsetting
    data = cik_list[cik_list['ticker']==ticker]['cik']
    data = data.values[0]

    # cik number received from source excludes 0s that comes first. Since cik is a 10-digit number, concatenate 0s.
    zeros = 10 - len(str(data))
    data = ('0' * zeros) + str(data)
    return data

def extract_numbers(taxonomy):
    data_dict = dict(financial_json_data['facts']['us-gaap'][taxonomy].items())
    # list to store data
    numbers = []

    for i in data_dict['units']['USD']:
        if 'frame' in i:
            # match annaual data 
            if re.match('CY\d*$', i['frame']):
                numbers.append(i['val'])

    return numbers

cik_url = 'https://www.sec.gov/files/company_tickers_exchange.json'
cik_list = cik.get_cik(cik_url)

# Getting data from SEC
# test for Apple Inc. 
cik_num = search_cik('AAPL')
url = f'https://data.sec.gov/api/xbrl/companyfacts/CIK{cik_num}.json'
headers = {'User-Agent' : 'Mozilla'}

res = requests.get(url, headers=headers)
financial_json_data = json.loads(res.text)

# Getting financial data
# test for Revenue
revenue_taxonomy = 'RevenueFromContractWithCustomerExcludingAssessedTax'
revenues = extract_numbers(revenue_taxonomy)
print(revenues)

# latest Revenue
def get_latest_number(data):
    return data[-1]

latest_revenue = get_latest_number(revenues)
print(latest_revenue)