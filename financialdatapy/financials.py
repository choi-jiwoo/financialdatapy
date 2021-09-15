from dateutil import parser
import pandas as pd
import json
from financialdatapy import request
from financialdatapy.filings import get_latest_form


class EmptyDataFrameError(Exception):
    """Exception when dataframe is empty.
    """
    pass


class ImbalanceNumberOfFactsError(Exception):
    """Exception when the number of elements and values are different.

    When a financial statement have N number of elements, values per period
    should also have N number of items.
    """
    pass


def get_financials(cik_num: str, submission: pd.DataFrame,
                   form_type: str = '10-K') -> tuple:
    """Get financial statements from either 10-K or 10-Q form.

    Args:
        cik_num: CIK of a company.
        submission: Dataframe containing all the company filings information.
        form_type: Either 10-K or 10-Q. Default value is 10-K.

    Returns:
        Tuple containing each financial statements data in dictionary.

    Raises:
        EmptyDataFrameError: If dataframe is empty.
    """

    form_type = form_type.upper()
    if not submission[submission['Form'] == form_type].empty:
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

        return income_statement, balance_sheet, cash_flow
    else:
        raise EmptyDataFrameError('Failed in getting financials.')


def get_values(link: str) -> dict:
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
    soup = res.get_soup()
    tbl = soup.find('table')

    header = tbl.find_all(class_='th')
    header = [x.get_text() for x in header]

    split_pt = 0
    for i, d in enumerate(header, start=1):
        try:
            parser.parse(d)
        except parser.ParserError:
            split_pt = i

    if split_pt == 0:
        month_ended = ['12 Months Ended']
        date = header
    else:
        month_ended = header[:split_pt]
        date = header[split_pt:]

    title = tbl.find(class_='tl').get_text()
    title, unit = title.split(' - ')

    element_tbl = tbl.find_all(class_='pl')
    element = [x.get_text() for x in element_tbl]

    values_tbl = tbl.find_all(class_=['nump', 'num', 'text'])
    all_values = [x.get_text().strip() for x in values_tbl]

    total_periods = len(date) % len(all_values)
    num_of_months_ended = len(date) // len(month_ended)
    num_of_values_per_period = len(all_values) // len(date)

    if len(element) == num_of_values_per_period:
        financials = {
            'title': title,
            'unit': unit,
            'element': element,
            'value': [],
        }
        for i, v in enumerate(month_ended):
            values_by_period = {
                date[x]: all_values[x::total_periods]
                for x
                in range(i*num_of_months_ended, (i+1)*num_of_months_ended)
            }
            financials['value'].append({v: values_by_period})

        return financials
    else:
        raise ImbalanceNumberOfFactsError(
            "Number of elements and values doesn't match")


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
