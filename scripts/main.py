from scripts import cik
from scripts import connect
from scripts import filings
from scripts import financials


def main():
    # Getting cik list
    cik_list = cik.get_cik()

    db = connect.connect_db()
    db.save_in_db(cik_list)

    # Getting data from SEC
    ticker = 'aapl'  # test for apple inc for the meantime
    cik_num = cik.search_cik(cik_list, ticker)

    # Getting list of submitted filings
    submission = filings.get_filings_list(cik_num)

    form_type = '10-K'  # test 10-K filing for the meantime

    # financial statemets as reported in SEC EDGAR
    income_statement, balance_sheet, cash_flow = filings.get_facts_by_form(
        cik_num,
        submission,
        form_type,
    )
    std_financial = financials.get_std_financials(
        ticker,
        which_financial='income_statement',  # test income statement for the meantime
        period='annual',
    )

    # Do something with these financial statements data...


if __name__ == '__main__':
    main()
