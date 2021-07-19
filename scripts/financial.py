import json
import requests
import re

# Getting data from SEC
# test for Apple Inc.
cik = '0000320193'
url = f'https://data.sec.gov/api/xbrl/companyfacts/CIK{cik}.json'
headers = {'User-Agent' : 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36'}

res = requests.get(url, headers=headers)
financial_json_data = json.loads(res.text)

# Getting financial data
def extract_numbers(taxonomy):
    data_dict = dict(financial_json_data['facts']['us-gaap'][taxonomy].items())
    numbers = []

    for i in data_dict['units']['USD']:
        if 'frame' in i:
            if re.match('CY\d*$', i['frame']):
                numbers.append(i['val'])

    return numbers

# test for Revenue
revenue_taxonomy = 'RevenueFromContractWithCustomerExcludingAssessedTax'
revenues = extract_numbers(revenue_taxonomy)
print(revenues)

# latest Revenue
def get_latest_number(data):
    return data[-1]

latest_revenue = get_latest_number(revenues)
print(latest_revenue)