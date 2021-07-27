from numpy import ushort
import financials
import filings

if __name__ == '__main__':
    # Getting cik list
    cik_list = filings.get_cik()

    # Getting data from SEC
    ticker = input('ticker : ') # should add test code later
    cik_num = filings.search_cik(cik_list, ticker)

    # Getting list of submitted filings 
    submission = filings.get_filings_list(cik_num)

    if submission[submission['Form']=='10-K'].empty: print('No 10-K submitted.')
    else:
        # get latest 10-K 
        latest_10K_filing = submission[submission['Form']=='10-K'].iloc[0].at['AccessionNumber']
        links = filings.get_latest_10K(cik_num, latest_10K_filing)

        # get facts
        is_l = links.get('income_statement')
        income_statement = financials.get_facts(is_l)

        bs_l = links.get('balance_sheet')
        balance_sheet = financials.get_facts(bs_l)

        cf_l = links.get('cash_flow')
        cash_flow = financials.get_facts(cf_l)


