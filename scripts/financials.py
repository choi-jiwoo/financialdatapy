import filings
from bs4 import BeautifulSoup
import pandas as pd
import re

def get_facts(link):
    res = filings.request_data(link)
    soup = BeautifulSoup(res.text, 'html.parser')
    tbl = soup.find('table')

    date = tbl.find_all(class_ = 'th')
    date = [x.get_text() for x in date]

    title = tbl.find(class_ = 'tl').get_text()
    title, unit = title.split(' - ')

    # remove element which is not a date
    pattern = 'balance\ssheet+s?'
    if re.search(pattern, title, flags = re.IGNORECASE) is None:
        date.pop(0)

    element_tbl = tbl.find_all(class_ = 'pl')
    element = [x.get_text() for x in element_tbl]

    facts_tbl = tbl.find_all(class_ = ['nump', 'num', 'text'])
    facts = [x.get_text().strip() for x in facts_tbl]
    years = len(date) % len(facts)

    facts_consecutive = dict({date[x] : facts[x::years] for x in range(0, years)})

    num_of_facts_y = len(facts) // len(date)
    
    if len(element) == num_of_facts_y:
        facts_df = pd.DataFrame(facts_consecutive, index = element)
    else :
        raise Exception('Number of elements and facts doesn\'t match')

    return facts_df