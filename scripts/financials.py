import yaml
import request


def get_standardized_financials(ticker):
    with open('config/config.yml', 'r') as f:
        config = yaml.safe_load(f)

    api_key = config['user']['financialmodelingprep_api_key']
    # list 3 major financials for the meantime. Must be modified soon
    ic = 'income-statement'
    bs = 'balance-sheet-statement'
    cf = 'cash-flow-statement'

    base_url = 'https://financialmodelingprep.com/api/v3/'
    param = f'{ic}/{ticker}?limit=120&apikey={api_key}'
    url = base_url + param
    financial_data = request.request_data(url, 'json')
