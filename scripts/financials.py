import yfinance as yf


def get_major_financials(ticker):
    company = yf.Ticker(ticker)

    company.info

    company.financials
    company.balance_sheet
    company.cashflow

    company.quarterly_financials
    company.quarterly_balance_sheet
    company.quarterly_cashflow
