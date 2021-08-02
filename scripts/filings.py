import request
import pandas as pd
import re

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
    url = ('https://www.sec.gov/cgi-bin/viewer?action=view&'\
           f'cik={cik}&accession_number={latest}&xbrl_type=v')
    soup = request.request_data(url, 'html')

    menu = soup.find(id='menu')
    a = menu.find_next('a', string='Financial Statements')
    ul = a.find_next('ul')
    li = ul.find_all('li')

    element = [x.get_text().lower() for x in li]
    filename = [re.search('r\d', str(x)).group().upper() for x in li]
    file_list = dict(zip(element, filename))

    # get links for 3 major financial statement.
    # ignore statements of comprehensive income,
    # parenthetical statement, and stockholder's equity
    ignore = ['parenthetical', 'comprehensive', 'stockholders']
    base_link = f'https://www.sec.gov/Archives/edgar/data/{cik}/{latest}/'
    links = {}

    for k, v in file_list.items():
        if any(x in k for x in ignore) == False:
            if re.search('income|operations?|earnings?', k, flags = re.I):
                links['income_statement'] = base_link + v + '.htm'
            elif re.search('balance\ssheets?|financial\sposition', k, flags = re.I):
                links['balance_sheet'] = base_link + v + '.htm'
            elif re.search('cash\sflows?', k, flags = re.I):
                links['cash_flow'] = base_link + v + '.htm'

    return links