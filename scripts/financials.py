import pandas as pd
from scripts import request


def get_std_financials(ticker: str,
                       which_financial: str,
                       period: str = 'annual') -> dict:
    financials = {
        'income_statement': 'I',
        'balance_sheet': 'B',
        'cash_flow': 'C',
    }
    periods = {
        'annual': 'A',
        'quarter': 'Q',
    }
    statement = financials[which_financial] + periods[period]
    url = f'https://finviz.com/api/statement.ashx?t={ticker}&s={statement}'
    data = request.request_data(url, 'json')

    del data['currency']
    del data['data']['Period Length']

    financial_statement = get_statements(data)

    return financial_statement


def get_statements(data: dict) -> pd.DataFrame():
    try:
        df = pd.DataFrame(data['data']).T
        df.columns = df.iloc[0, :].values
        df.drop(df.index[[0]], axis=0, inplace=True)
        df = df.replace(',', '', regex=True)

        for i in df:
            df[i] = pd.to_numeric(df[i])

        values_unit = 1_000_000
        df = df * values_unit
    except Exception as e:
        print(e)

    return df
