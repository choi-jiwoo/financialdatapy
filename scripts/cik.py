import pandas as pd
import request

def get_cik():
    url = 'https://www.sec.gov/files/company_tickers_exchange.json'
    data = request.request_data(url, 'json')
    
    cik_list = pd.DataFrame(data['data'], columns=data['fields'])
    cik_list['cik'] = cik_list['cik'].astype(str)
    cik_list['name'] = cik_list['name'].str.lower().str.title()

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