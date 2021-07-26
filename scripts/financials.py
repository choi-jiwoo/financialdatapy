import filings
from bs4 import BeautifulSoup
import pandas as pd

def get_facts(link):
    res = filings.request_data(link)
    soup = BeautifulSoup(res.text)

    tbl = soup.find('table')
    # which financial
    title = tbl.find(class_='tl').get_text()
    # index 0 : which financial
    # index 1: unit (USD)
    title.split(' - ')

    # date
    date = tbl.find_all(class_='th')
    date = [x.get_text() for x in date]
    date.pop(0) # remove unnecessary

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

    return facts_df