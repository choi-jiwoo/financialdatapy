import pandas as pd
from scripts import request


def get_std_financials(ticker: str, which_financial: str) -> pd.DataFrame:
    period = {
        'annual': '1',
        'quarter': '2'
    }
    financials = {
        'ic': 'incomeStatementTable',
        'bs': 'balanceSheetTable',
        'cf': 'cashFlowTable'
    }

    url = ('https://api.nasdaq.com/api/company/'
           f'{ticker}/financials?frequency={period["annual"]}')
    data = request.request_data(url, 'json')

    financial_statement = get_statements(data, financials[which_financial])

    return financial_statement


def get_statements(data: dict, financials_name: str) -> pd.DataFrame:
    try:
        financial = data['data'][financials_name]
        df = pd.DataFrame(financial['rows'])
        df.columns = financial['headers'].values()
        df.index = df.iloc[:, 0]
        df.drop(df.columns[[0]], axis=1, inplace=True)

        return df
    except Exception as e:
        print(e)
        return
