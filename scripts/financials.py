import re
import filings
from bs4 import BeautifulSoup

def get_facts(cik, filing, link):
    

def get_latest_10K(cik, latest):
    url = f'https://www.sec.gov/cgi-bin/viewer?action=view&cik={cik}&accession_number={latest}&xbrl_type=v'
    res = filings.request_data(url)
    soup = BeautifulSoup(res.text)

    menu = soup.find(id='menu')
    a = menu.find_next('a', string='Financial Statements')
    ul = a.find_next('ul')
    li = ul.find_all('li')

    # element names in financial statements
    element = [x.get_text() for x in li]
    # filenames of each 3 statements
    filename = [re.search('r\d', str(x)).group().upper() for x in li]
    file_list = list(zip(element, filename))

    # remain links only income statements, cash flows, and balance sheets
    filename_dict = {}
    pattern = '((((?<!comprehensive)\sincome)|operation+s?|earning+s?)|(cash\sflow+s?)|(balance\ssheet+s?))(?!\(parenthetical+s?\))([a-z0-9]+)$'
    regex = re.compile(pattern, flags=re.IGNORECASE)

    for i in file_list:
        if regex.search(i[0]):
            filename_dict[i[0]] = f'https://www.sec.gov/Archives/edgar/data/{cik}/{latest}/{i[1]}.htm'
    
    get_facts(cik, latest, filename_dict)