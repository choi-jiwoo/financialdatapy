import pandas as pd
import request
import string
import re

def get_cik():
    url = 'https://www.sec.gov/files/company_tickers_exchange.json'
    data = request.request_data(url, 'json')
    
    cik_list = pd.DataFrame(data['data'], columns=data['fields'])
    
    cik_list['exchange'] = cik_list['exchange'].str.upper()
    cik_list = cik_list[
        (cik_list['exchange'] == 'NASDAQ') | (cik_list['exchange'] == 'NYSE')
    ]
    cik_list = cik_list.reset_index(drop=True)
    # remove exchange column
    cik_list = cik_list.iloc[:,:-1]

    cik_list['cik'] = cik_list['cik'].astype(str)

    # remove all characters after '\' or '/' in a company name
    pattern = r'\s?(\/|\\)[a-zA-Z]*'
    regex = re.compile(pattern, flags = re.I)
    cik_list['name'] = [string.capwords(x) for x in cik_list['name']]
    cik_list['name'] = [regex.sub('', x) for x in cik_list['name']]

    return cik_list

def search_cik(cik_list, ticker):
    ticker = ticker.upper()
    data = cik_list[cik_list['ticker']==ticker]['cik']
    data = data.values[0]

    # cik number received from source excludes 0s that comes first.
    # Since cik is a 10-digit number, concatenate 0s.
    zeros = 10 - len(str(data))
    data = ('0' * zeros) + str(data)

    return data