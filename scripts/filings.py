from dateutil.parser import parse
import pandas as pd
import re
from scripts import request


def get_filings_list(cik):
    url = f'http://data.sec.gov/submissions/CIK{cik}.json'
    data = request.request_data(url, 'json')
    info = data['filings']['recent']

    acc = info['accessionNumber']
    acc = [s.replace('-', '') for s in acc]
    form = info['form']
    doc = info['primaryDocument']
    date = info['filingDate']

    filings = pd.DataFrame(
        zip(acc, form, doc, date),
        columns=['AccessionNumber', 'Form', 'PrimaryDocument', 'Date']
    )

    return filings


# only for the latest filing
def get_latest_form(cik, latest):
    url = ('https://www.sec.gov/cgi-bin/viewer?action=view&'
           f'cik={cik}&accession_number={latest}&xbrl_type=v')
    soup = request.request_data(url, 'html')

    menu = soup.find(id='menu')
    a = menu.find_next('a', string='Financial Statements')
    ul = a.find_next('ul')
    li = ul.find_all('li')

    element = [x.get_text() for x in li]
    filename = [
        re.search(r'r\d', str(x), flags=re.I).group().upper() for x in li
    ]
    file_list = dict(zip(element, filename))

    # get links for 3 major financial statement.
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


def get_facts_by_form(cik_num, submission, form_type):
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
        raise Exception('Failed in getting facts.')


def get_facts(link):
    soup = request.request_data(link, 'html')
    tbl = soup.find('table')

    facts_hdr = tbl.find_all(class_='th')
    facts_hdr = [x.get_text() for x in facts_hdr]

    split_pt = 0
    for i, d in enumerate(facts_hdr, start=1):
        try:
            parse(d)
        except Exception:
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
            'facts': []
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
        raise Exception("Number of elements and facts doesn't match")
