import pandas as pd
from string import capwords
import re
import request


def get_cik():
    url = 'https://www.sec.gov/files/company_tickers_exchange.json'
    cik_data = request.request_data(url, 'json')

    cik_list = pd.DataFrame(cik_data['data'], columns=cik_data['fields'])

    cik_list['exchange'] = cik_list['exchange'].str.upper()
    cik_list = cik_list[
        (cik_list['exchange'] == 'NASDAQ') | (cik_list['exchange'] == 'NYSE')
    ]
    cik_list = cik_list.reset_index(drop=True)
    cik_list = cik_list.drop('exchange', axis=1)

    cik_list['cik'] = cik_list['cik'].astype(str)

    # remove all characters after '\' or '/' in a company name
    # ex) Qualcomm inc\de -> Qualcomm inc
    pattern = r'\s?(\/|\\)[a-zA-Z]*'
    regex = re.compile(pattern, flags=re.I)
    cik_list['name'] = [regex.sub('', x) for x in cik_list['name']]

    # comapany names in Title Case
    cik_list['name'] = [capwords(x) for x in cik_list['name']]

    return cik_list


def search_cik(cik_list, ticker):
    ticker = ticker.upper()
    ticker_df = cik_list[cik_list['ticker'] == ticker]
    cik = ticker_df.get('cik').item()

    # cik number received from source excludes 0s that comes first.
    # Since cik is a 10-digit number, concatenate 0s.
    zeros = 10 - len(str(cik))
    cik = ('0' * zeros) + str(cik)

    return cik
