import pandas as pd
import json
from scripts import request


def get_std_financials(ticker: str,
                       which_financial: str,
                       period: str = 'annual') -> pd.DataFrame:
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
    res = request.Request(url)
    data = res.get_json()

    financial_statement = convert_to_table(data)

    return financial_statement


def convert_to_table(data: dict) -> pd.DataFrame:
    del data['currency']
    if 'Period Length' in data['data']:
        del data['data']['Period Length']

    df = pd.DataFrame(data['data']).T
    date = df.iloc[0, :].values
    df.columns = date
    row_with_dates = df.index[[0]]
    df.drop(row_with_dates, axis='index', inplace=True)

    df = df.replace(',', '', regex=True)
    for i in df:
        df[i] = pd.to_numeric(df[i])

    values_unit = 1_000_000
    df = df * values_unit

    ignore_word = ['eps', 'employee', 'number']
    for i in df.index:
        for word in ignore_word:
            if word in i.lower():
                df.loc[i] /= 1_000_000

    return df


def convert_into_korean(statement: pd.DataFrame) -> pd.DataFrame:
    # elements of financial statements mapped with translation in korean.
    with open('data/statements_kor.json', 'r') as f:
        stmts_in_kor = json.load(f)

    for i in statement.index:
        statement.rename(index={i: stmts_in_kor[i]}, inplace=True)

    return statement
