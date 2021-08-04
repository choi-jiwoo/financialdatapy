from dateutil.parser import parse
import filings
import request


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
            'element': element
        }
        for i, v in enumerate(month_ended):
            facts_by_period = {
                date[x]:
                    all_facts[x::facts_col]
                    for x
                    in range(i*periods, (i+1)*periods)
            }
            facts['facts'] = {v: facts_by_period}

        return facts
    else:
        raise Exception("Number of elements and facts doesn't match")


def get_form_facts(cik_num, submission, form_type):
    if not submission[submission['Form'] == form_type].empty:
        # get latest 10-K
        form = submission[submission['Form'] == form_type]
        latest_filing = form.iloc[0].at['AccessionNumber']
        links = filings.get_latest_form(cik_num, latest_filing)

        # get facts
        is_l = links.get('income_statement')
        income_statement = get_facts(is_l)

        bs_l = links.get('balance_sheet')
        balance_sheet = get_facts(bs_l)

        cf_l = links.get('cash_flow')
        cash_flow = get_facts(cf_l)

        return income_statement, balance_sheet, cash_flow
    else:
        raise Exception('Failed in getting facts.')
