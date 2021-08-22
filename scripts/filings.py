from dateutil import parser
import pandas as pd
import re
from scripts import request


class EmptyDataFrameError(Exception):
    """Exception when dataframe is empty.
    """
    pass


class ImbalanceNumberOfFactsError(Exception):
    """Exception when the number of elements and facts are different.

    When a financial statement have N number of elements, facts data per period
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


def get_facts_by_form(cik_num: str, submission: pd.DataFrame,
                      form_type: str) -> dict:
    """Get facts from either 10-K or 10-Q form.

    Args:
        cik_num: CIK of a company.
        submission: Dataframe containing all the company filings information.
        form_type: Either 10-K or 10-Q.

    Returns:
        Dictionary of each financial statements data.

    Raises:
        EmptyDataFrameError: If dataframe is empty.
    """

    if not submission[submission['Form'] == form_type].empty:
        # get latest filing
        form = submission[submission['Form'] == form_type]
        latest_filing = form.iloc[0].at['AccessionNumber']
        links = get_latest_form(cik_num, latest_filing)

        is_l = links.get('income_statement')
        income_statement = get_facts(is_l)

        bs_l = links.get('balance_sheet')
        balance_sheet = get_facts(bs_l)

        cf_l = links.get('cash_flow')
        cash_flow = get_facts(cf_l)

        return income_statement, balance_sheet, cash_flow
    else:
        raise EmptyDataFrameError('Failed in getting facts.')


def get_facts(link: str) -> dict:
    """Extract a financial statement data from web.

    Args:
        link: URL that has financial statment data in a table form.

    Returns:
        Dictionary containing all the data from financial statement.

    Raises:
        ImbalanceNumberOfFactsError: When the number of elements and facts
            are different.
    """

    res = request.Request(link)
    soup = res.get_soup()
    tbl = soup.find('table')

    facts_hdr = tbl.find_all(class_='th')
    facts_hdr = [x.get_text() for x in facts_hdr]

    split_pt = 0
    for i, d in enumerate(facts_hdr, start=1):
        try:
            parse(d)
        except parser.ParserError:
            split_pt = i

    if split_pt == 0:
        month_ended = ['12 Months Ended']
        date = facts_hdr
    else:
        month_ended = facts_hdr[:split_pt]
        date = facts_hdr[split_pt:]

    title = tbl.find(class_='tl').get_text()
    title, unit = title.split(' - ')

    element_tbl = tbl.find_all(class_='pl')
    element = [x.get_text() for x in element_tbl]

    facts_tbl = tbl.find_all(class_=['nump', 'num', 'text'])
    # facts for all periods
    all_facts = [x.get_text().strip() for x in facts_tbl]

    facts_col = len(date) % len(all_facts)
    periods = len(date) // len(month_ended)
    num_of_facts = len(all_facts) // len(date)

    if len(element) == num_of_facts:
        facts = {
            'title': title,
            'unit': unit,
            'element': element,
            'facts': [],
        }
        for i, v in enumerate(month_ended):
            facts_by_period = {
                date[x]:
                    all_facts[x::facts_col]
                    for x
                    in range(i*periods, (i+1)*periods)
            }
            facts['facts'].append({v: facts_by_period})

        return facts
    else:
        raise ImbalanceNumberOfFactsError(
            "Number of elements and facts doesn't match")
