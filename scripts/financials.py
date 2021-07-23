import re
import filings
from bs4 import BeautifulSoup

def get_latest_10K(cik, latest):
    url = f'https://www.sec.gov/cgi-bin/viewer?action=view&cik={cik}&accession_number={latest}&xbrl_type=v'
    res = filings.request_data(url)
    soup = BeautifulSoup(res.text)

    financial_stmt = soup.find(id='menu_cat3')
    ul = financial_stmt.find_next('ul')
    li = ul.find_all('li')

    financials_name = [x.get_text() for x in li]
    file_names = [re.search('r\d', str(x)).group().upper() for x in li]

    get_facts(cik, latest, file_names)

def get_facts(cik, filing, file_names):
    # test just for one statment for now
    file = file_names[0]
    url = f'https://www.sec.gov/Archives/edgar/data/{cik}/{filing}/{file}.htm'
    
    # scrape codes ...

    