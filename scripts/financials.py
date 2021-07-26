import filings
from bs4 import BeautifulSoup
import pandas as pd
import re

def get_facts(link):
    res = filings.request_data(link)
    soup = BeautifulSoup(res.text, 'html.parser')
    tbl = soup.find('table')

    # date
    date = tbl.find_all(class_='th')
    date = [x.get_text() for x in date]

    title = tbl.find(class_='tl').get_text()

    # remove unnecessary
    if re.search('balance\ssheet+s?', title, flags=re.IGNORECASE) is None:
        date.pop(0)

    # element names
    element_tbl = tbl.find_all(class_='pl')
    element = [x.get_text() for x in element_tbl]
    # facts
    facts_tbl = tbl.find_all(class_=['nump', 'num', 'text'])
    facts = [x.get_text().strip() for x in facts_tbl]

    num_of_facts_y = len(facts) // len(date)
    years = len(date)%len(facts)

    # key = date : value = facts
    facts_consecutive = dict({date[x] : facts[x::years] for x in range(0,years)})

    # check if number of elements in a financial statement match with number of facts
    if len(element) == num_of_facts_y:
        facts_df = pd.DataFrame(facts_consecutive, index=element)
    else :
        raise Exception('Number of elements and facts doesn\'t match')

    return facts_df