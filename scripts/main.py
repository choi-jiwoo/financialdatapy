from scripts import cik
from scripts import connect
from scripts import filings


def main():
    # Getting cik list
    cik_list = cik.get_cik()

    db = connect.connect_db()
    db.save_in_db(cik_list)

    # Getting data from SEC
    ticker = 'aapl'  # test for apple inc. for meantime
    cik_num = cik.search_cik(cik_list, ticker)

    # Getting list of submitted filings
    submission = filings.get_filings_list(cik_num)

    form_type = '10-K'
    income_statement, balance_sheet, cash_flow = filings.get_facts_by_form(
        cik_num,
        submission,
        form_type  # test for 10-K filing for meantime
    )

    # Do something with these financial statements data...
    print(income_statement)
    print(balance_sheet)
    print(cash_flow)


if __name__ == '__main__':
    main()
