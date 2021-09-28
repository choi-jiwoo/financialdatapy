"""This module retrieves a list of companies CIK."""
import pandas as pd
from string import capwords
import re
from financialdatapy import request


class NeedsUpdateError(Exception):
    """Raises error if cik list needs to be updated to the latest."""

    pass


def get_cik_list(update: bool = False) -> pd.DataFrame:
    """Get cik_list.csv saved in local.

    If it is not saved in local, retrieve the data from SEC.

    :param update: Updates cik list to the latest cik list, defaults to False.
    :type update: bool
    :return: Dataframe with CIK, company name, and ticker for its columns.
    :rtype: pandas.DataFrame
    """
    try:
        if update:
            raise NeedsUpdateError()
        cik_list = pd.read_csv('data/cik_list.csv')
    except (FileNotFoundError, NeedsUpdateError):
        cik_list = get_cik()
        cik_list.to_csv('data/cik_list.csv', index=False)

    return cik_list


def get_cik() -> pd.DataFrame:
    """Get a list of companies CIK(Central Index Key) from SEC.

    The list also contains ticker of a company.

    :return: Dataframe with CIK, company name, and ticker for its columns.
    :rtype: pandas.DataFrame
    """
    url = 'https://www.sec.gov/files/company_tickers_exchange.json'
    res = request.Request(url)
    cik_data = res.get_json()

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


def search_cik(cik_list: pd.DataFrame, ticker: str) -> str:
    """Search CIK of specific a company.

    :param cik_list: Dataframe containing CIK, company name,
        and ticker for its columns.
    :type cik_list: pandas.DataFrame
    :param ticker: Company ticker to search.
    :type ticker: str
    :return: CIK of the company searching for.
    :rtype: str
    """
    ticker_df = cik_list[cik_list['ticker'] == ticker]
    cik = ticker_df.get('cik').item()

    # cik number received from source excludes 0s that comes first.
    # Since cik is a 10-digit number, concatenate 0s.
    zeros = 10 - len(str(cik))
    cik = ('0' * zeros) + str(cik)

    return cik
