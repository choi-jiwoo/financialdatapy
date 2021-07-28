import filings
import re
import pandas as pd
from bs4 import BeautifulSoup
from dateutil.parser import parse

def get_facts(link):
    res = filings.request_data(link)
    soup = BeautifulSoup(res.text, 'html.parser')
    tbl = soup.find('table')

    facts_hdr = tbl.find_all(class_ = 'th')
    facts_hdr = [x.get_text() for x in facts_hdr]

    title = tbl.find(class_ = 'tl').get_text()
    title, unit = title.split(' - ')

    for i, date in enumerate(facts_hdr):
        try:
            parse(date)
        except:
            facts_hdr.pop(i)

    element_tbl = tbl.find_all(class_ = 'pl')
    element = [x.get_text() for x in element_tbl]

    facts_tbl = tbl.find_all(class_ = ['nump', 'num', 'text'])
    facts = [x.get_text().strip() for x in facts_tbl]
    years = len(facts_hdr) % len(facts)

    consecutive_facts = dict({facts_hdr[x] : facts[x::years] for x in range(0, years)})

    num_of_facts_y = len(facts) // len(facts_hdr)
    
    if len(element) == num_of_facts_y:
        facts_df = pd.DataFrame(consecutive_facts, index = element)
    else :
        raise Exception('Number of elements and facts doesn\'t match')

    return facts_df