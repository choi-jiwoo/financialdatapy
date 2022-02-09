"""This module retrieves company filings data from EDGAR."""
from functools import lru_cache
import pandas as pd
import re
from financialdatapy.request import Request


@lru_cache
def get_filings_list(cik: str) -> pd.DataFrame:
    """Retrieve whole list of filings a company made in the SEC EDGAR system.

    :param cik: CIK of a company.
    :type cik: str
    :return: Dataframe containing all the company filings data.
    :rtype: pandas.DataFrame
    """
    url = f'http://data.sec.gov/submissions/CIK{cik}.json'
    res = Request(url)
    data = res.get_json()
    info = data['filings']['recent']

    acc = info['accessionNumber']
    acc = [s.replace('-', '') for s in acc]
    form = info['form']
    doc = info['primaryDocument']
    date = info['filingDate']

    filings = pd.DataFrame(
        zip(acc, form, doc, date),
        columns=['AccessionNumber', 'Form', 'PrimaryDocument', 'Date'],
    )

    return filings


def get_latest_form(cik: str, latest: str) -> dict:
    """Find URL of each financial statements where their data is in table form.

    EDGAR system provides an 'interactive data' in their website. It contains
    financial statements as reported in table form.


    :param cik: CIK of a company.
    :type cik: str
    :param latest: Latest accesion number of a form.
    :type cik: str
    :return: Each financial statements mapped with their URL to the data.
    :rtype: dict
    """
    url = ('https://www.sec.gov/cgi-bin/viewer?action=view&'
           f'cik={cik}&accession_number={latest}&xbrl_type=v')
    res = Request(url)
    soup = res.get_soup()

    menu = soup.find(id='menu')
    a = menu.find_next('a', string='Financial Statements')
    ul = a.find_next('ul')
    li = ul.find_all('li')

    element = [x.get_text() for x in li]
    filename = [
        re.search(r'r\d', str(x), flags=re.I).group().upper() for x in li
    ]
    file_list = dict(zip(element, filename))

    # get links for 3 major financial statement only.
    # ignore statements of comprehensive income,
    # parenthetical statement, and stockholder's equity
    ignore = ['parenthetical', 'comprehensive', 'stockholders']
    base_link = f'https://www.sec.gov/Archives/edgar/data/{cik}/{latest}/'
    links = {}

    for k, v in file_list.items():
        if any(x in k.lower() for x in ignore):
            continue

        if re.search(r'income|operations?|earnings?', k, flags=re.I):
            links['income_statement'] = base_link + v + '.htm'
        elif re.search(r'balance\ssheets?|financial\sposition', k, flags=re.I):
            links['balance_sheet'] = base_link + v + '.htm'
        elif re.search(r'cash\sflows?', k, flags=re.I):
            links['cash_flow'] = base_link + v + '.htm'

    return links
