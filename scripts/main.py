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
    ticker = input('ticker : ') # should add test code later
    cik_num = cik.search_cik(cik_list, ticker)

    # Getting list of submitted filings 
    submission = filings.get_filings_list(cik_num)

    income_statement, balance_sheet, cash_flow = financials.get_10K_facts(
        cik_num,
        submission
    )
    
    # Do something with these financial statements data...

if __name__ == '__main__':
    main()