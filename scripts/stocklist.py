import pandas as pd
import requests
from bs4 import BeautifulSoup
from decouple import config
from sqlalchemy import create_engine

def convert_to_dataframe(s, exchange_name):
    """convert data received from source into a dataframe

    Args:
        s (session): http request session
        exchange_name (string): stock exchange stock list to get

    Returns:
        dataframe: stock list of the stock exchange
    """
    # get .txt formed data
    text_data = s.get('http://www.eoddata.com/Data/symbollist.aspx?e='+exchange_name)
    row_splitted = text_data.text.split('\r\n')
    exchange = pd.DataFrame([x.split('\t') for x in row_splitted], columns=['Symbol', 'Description'])
    # remove duplicated header and blank row at the end
    exchange = exchange.drop([exchange.index[0], exchange.index[-1]])
    # add exchange name
    name = pd.Series([exchange_name], name='Exchange')
    exchange = exchange.merge(name, how='cross')

    return (exchange)

def check_diff(stock_list):
    """check difference between latest stock list and past stock list since market changes every day

    Args:
        stock_list (dataframe): stock list of all 3 major stock exchanges
    """
    stock_list.to_csv('stock_list_210705.csv', index=False)
    
    # check changes in stock list
    old = pd.read_csv('stock_list_210701.csv')
    print(f'yesterday : {len(old)}, today : {len(stock_list)}')

    # check which stock is changed
    # 'left_only': removed from stock exchange 
    # 'right_only': newly listed in stock exchange
    merged = pd.merge(old,stock_list, how='outer', indicator=True)
    print(merged[merged['_merge'] != 'both'])

def get_stock_list():
    """get stock list data from eoddata.com

    Returns:
        stock_list: stock list of all 3 major stock exchanges
    """
    # login information to be passed into HTML requests
    url = 'http://www.eoddata.com/symbols.aspx'
    exchange = ['NYSE', 'NASDAQ', 'AMEX']
    # get login information from config file
    username = config('username', default='')
    password = config('password', default='')
    # basic form data to pass when sending POST request
    payload = {
        'ctl00$cph1$ls1$txtEmail' : username,
        'ctl00$cph1$ls1$txtPassword' : password,
        'ctl00$cph1$ls1$btnLogin': 'Login'
    }

    # use Session() to make multiple requests
    with requests.Session() as s:
        page = s.get(url)
        soup = BeautifulSoup(page.content, 'html.parser')
        # additional form data passed for ASP.NET based website
        payload['__VIEWSTATE'] = soup.select_one('#__VIEWSTATE')['value']
        payload['__VIEWSTATEGENERATOR'] = soup.select_one('#__VIEWSTATEGENERATOR')['value']
        payload['__EVENTVALIDATION'] = soup.select_one('#__EVENTVALIDATION')['value']

        res = s.post(url, data=payload)

        validation = BeautifulSoup(res.content, 'html.parser')
        logout = validation.select_one('#ctl00_cph1_ls1_lnkLogOut')

        if logout is None:
            print('Log in failed')

        elif logout.text.lower() == 'log out':
            nyse = convert_to_dataframe(s, exchange[0])
            nasdaq = convert_to_dataframe(s, exchange[1])
            amex = convert_to_dataframe(s, exchange[2])

            # make as one dataframe
            nasdaq_amex = [nasdaq, amex]
            stock_list = nyse.append(nasdaq_amex, ignore_index=True)
            
            # remove duplicated stocks across three different exchange
            stock_list = stock_list.drop_duplicates(subset=['Symbol'], ignore_index=True)
            
            # check_diff(stock_list)
    
    return (stock_list)
