import filings
import request
from dateutil.parser import parse

def get_facts(link):
    soup = request.request_data(link, 'html')
    tbl = soup.find('table')

    facts_hdr = tbl.find_all(class_ = 'th')
    facts_hdr = [x.get_text() for x in facts_hdr]

    title = tbl.find(class_ = 'tl').get_text()
    title, unit = title.split(' - ')

    split_pt = 0
    for i, d in enumerate(facts_hdr):
        try:
            parse(d)
        except:
            split_pt = i

    if split_pt == 0:
        month_ended = ['12 Months Ended']
        date = facts_hdr
    else:
        month_ended = facts_hdr[:split_pt + 1]
        date = facts_hdr[split_pt + 1:]

    element_tbl = tbl.find_all(class_ = 'pl')
    element = [x.get_text() for x in element_tbl]

    facts_tbl = tbl.find_all(class_ = ['nump', 'num', 'text'])
    facts = [x.get_text().strip() for x in facts_tbl]

    facts_col = len(date) % len(facts)
    period = len(date) // len(month_ended)
    
    facts_dict = {}
    for i, v in enumerate(month_ended):
        facts_dict[v] = {date[x] : facts[x::facts_col] for x in range(i*period, (i+1)*period)}

    num_of_facts_y = len(facts) // len(date)
    
    if len(element) == num_of_facts_y:
        return facts_dict
    else :
        raise Exception("Number of elements and facts doesn't match")

def get_10K_facts(cik_num, submission):
    if submission[submission['Form']=='10-K'].empty: print('No 10-K submitted.')
    else:
        # get latest 10-K 
        form_10K = submission[submission['Form']=='10-K']
        latest_10K_filing = form_10K.iloc[0].at['AccessionNumber']
        links = filings.get_latest_10K(cik_num, latest_10K_filing)

        # get facts
        is_l = links.get('income_statement')
        income_statement = get_facts(is_l)

        bs_l = links.get('balance_sheet')
        balance_sheet = get_facts(bs_l)

        cf_l = links.get('cash_flow')
        cash_flow = get_facts(cf_l)

    return income_statement, balance_sheet, cash_flow