import financials
import filings
import cik
import connect

def main():
    # Getting cik list
    cik_list = cik.get_cik()

    db = connect.connect_db()
    db.save_in_db(cik_list)

    # Getting data from SEC
    ticker = 'aapl' # test for apple inc. for meantime
    cik_num = cik.search_cik(cik_list, ticker)

    # Getting list of submitted filings 
    submission = filings.get_filings_list(cik_num)

    income_statement, balance_sheet, cash_flow = financials.get_form_facts(
        cik_num,
        submission,
        '10-K'  # test for 10-K filing for meantime
    )
    
    # Do something with these financial statements data...

if __name__ == '__main__':
    main()