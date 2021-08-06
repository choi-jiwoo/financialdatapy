import yfinance as yf
import yaml
import request


def get_major_financials_yfinance(ticker):
    company = yf.Ticker(ticker)

    company.info

    company.financials
    company.balance_sheet
    company.cashflow

    company.quarterly_financials
    company.quarterly_balance_sheet
    company.quarterly_cashflow


def get_major_financials_alphavantage(ticker):
    with open('config/config.yml', 'r') as f:
        config = yaml.safe_load(f)

    api_key = config['user']['alphavantage_api']
    which = ['OVERVIEW', 'INCOME_STATEMENT', 'BALANCE_SHEET', 'CASH_FLOW']
    url = ('https://www.alphavantage.co/query?'
           f'function={which[3]}&symbol={ticker}&apikey={api_key}')

    financial_data = request.request_data(url, 'json')
