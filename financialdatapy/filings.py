from dateutil import parser
import pandas as pd
import re
from financialdatapy import request


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


def get_filings_list(cik: str) -> pd.DataFrame:
    """Retrieve whole list of filings a company made in the SEC EDGAR system.

    Args:
        cik: CIK of a company.

    Returns:
        Dataframe containing all the company filings information.
    """

    url = f'http://data.sec.gov/submissions/CIK{cik}.json'
    res = request.Request(url)
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

    EDGAR system provides an interactive data in their website. Interactive
    data only contains the financial statements of a company which is just the
    same one in the official document. So it makes one easy to scrape the
    financial statment data.

    Args:
        cik: CIK of a company.
        latest: Latest accesion number of a form.

    Returns:
        Dictionary with the name of financial statements as a key, and their
            URL to the data as a value.
    """

    url = ('https://www.sec.gov/cgi-bin/viewer?action=view&'
           f'cik={cik}&accession_number={latest}&xbrl_type=v')
    res = request.Request(url)
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


def get_financials(cik_num: str, submission: pd.DataFrame,
                   form_type: str = '10-K') -> dict:
    """Get financial statements from either 10-K or 10-Q form.

    Args:
        cik_num: CIK of a company.
        submission: Dataframe containing all the company filings information.
        form_type: Either 10-K or 10-Q. Default value is 10-K.

    Returns:
        Dictionary of each financial statements data.

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
