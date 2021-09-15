import pandas as pd
import json
from financialdatapy import request
from financialdatapy.filings import get_latest_form


class EmptyDataFrameError(Exception):
    """Exception when dataframe is empty.
    """
    pass


def get_financials(cik_num: str, submission: pd.DataFrame,
                   form_type: str = '10-K') -> dict:
    """Get financial statements from either 10-K or 10-Q form.

    Args:
        cik_num: CIK of a company.
        submission: Dataframe containing all the company filings information.
        form_type: Either 10-K or 10-Q. Default value is 10-K.

    Returns:
        Dictionary containing each financial statements data in dictionary.

    Raises:
        EmptyDataFrameError: If dataframe is empty.
    """

    form_type = form_type.upper()

    if submission[submission['Form'] == form_type].empty:
        raise EmptyDataFrameError('Failed in getting financials.')

    # get latest filing
    form = submission[submission['Form'] == form_type]
    latest_filing = form.iloc[0].at['AccessionNumber']
    links = get_latest_form(cik_num, latest_filing)

    is_l = links.get('income_statement')
    income_statement = get_values(is_l)

    bs_l = links.get('balance_sheet')
    balance_sheet = get_values(bs_l)

    cf_l = links.get('cash_flow')
    cash_flow = get_values(cf_l)

    financial_statements = {
        'income_statement': income_statement,
        'balance_sheet': balance_sheet,
        'cash_flow': cash_flow,
    }

    return financial_statements


def get_values(link: str) -> pd.DataFrame:
    """Extract a financial statement values from web.

    Args:
        link: URL that has financial statment data in a table form.

    Returns:
        Dictionary containing all the data from financial statement.

    Raises:
        ImbalanceNumberOfFactsError: When the number of elements and values
            are different.
    """
    res = request.Request(link)
    df = pd.read_html(res.res.text)[0]

    first_column = df.columns[0]
    multi_index = len(first_column)

    if multi_index == 2:
        first_column_header = df.columns[0][0]
    else:
        first_column_header = df.columns[0]

    title, unit = first_column_header.split(' - ')
    new_column_name = df.iloc[:, 0].rename((title, unit))

    df = df.drop(columns=df.columns[0])
    df.insert(
        loc=0,
        column=new_column_name.name,
        value=[*new_column_name.values],
        allow_duplicates=True,
    )

    df = df.fillna('')

    from_element = 1
    df.iloc[:, from_element:] = df.iloc[:, from_element:].apply(
        lambda x: [
            ''.join(filter(str.isdigit, i))
            for i
            in x
        ]
    )

    return df


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
