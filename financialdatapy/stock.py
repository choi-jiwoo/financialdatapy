"""Retrieve data of a certain stock.

Scrape data from 3 major financial statements as reported in the SEC EDGAR
system, 3 major standard financial statements from finviz.com,
and a historical price data of a stock (company).

Classes:
    Cik
    Stock

Get a list of CIK:

    from financialdatapy.stock import Cik

    Cik.update_cik_list()  # get latest cik list
    cik_list = Cik.cik_list

Get financial statements:

    from financialdatapy.stock import Stock

    comp = Stock('AAPL')
    aapl_ic_as_reported = comp.financials('10-K', 'income_statement')
    aapl_std_ic = comp.standard_financials('income_statement', 'annual')

Get historical price data:

    from financialdatapy.stock import Stock

    comp = Stock('AAPL')
    price = comp.historical('2021-1-1', '2021-2-1')
"""
import pandas as pd
from typing import Optional
from financialdatapy.cik import get_cik_list
from financialdatapy.cik import search_cik
from financialdatapy.filings import get_filings_list
from financialdatapy.financials import UsFinancials
from financialdatapy.price import UsMarket


class Cik():
    """Cik list as a class variable."""

    cik_list = get_cik_list()

    @staticmethod
    def update_cik_list():
        """Get the latest cik list from SEC."""
        Cik.cik_list = get_cik_list(update=True)


class Stock(Cik):
    """Class representing a stock or a company.

    Attributes:
        ticker: Ticker of a company/stock.
    """

    def __init__(self, ticker: str) -> None:
        """Initialize ticker to search.

        Args:
            ticker: Ticker of a stock.
        """

        self.ticker = ticker.upper()

    def financials(self, form: str = '10-K',
                   financial: str = 'income_statement') -> pd.DataFrame:
        """Get financial statements as reported.

        Args:
            form: Either '10-K' or '10-Q' form. Default value is '10-K'.
            financial: Which financial statement to retrieve. Input string
                should be either 'income_statement', 'balance_sheet', or
                'cash_flow'. Default value is 'income_statement'

        Returns:
            A dataframe containing financial statement as reported.
        """

        comp_cik = search_cik(Stock.cik_list, self.ticker)
        submission = get_filings_list(comp_cik)
        name = ['income_statement', 'balance_sheet', 'cash_flow']

        market = UsFinancials()
        financial_statement = market.get_financials(
            cik_num=comp_cik,
            submission=submission,
            form_type=form,
        )

        return financial_statement[financial]

    def standard_financials(self, which_financial: str = 'income_statement',
                            period: str = 'annual') -> pd.DataFrame:
        """Get standard financial statements.

        Args:
            which_financial: One of the three financial statement.
                'income_statement' or 'balance_sheet' or 'cash_flow'. Default
                value is 'income_statement'
            period: Either 'annual' or 'quarter'. Default value is 'annual'

        Returns:
            Dataframe with columns as dates, and index as financial
            statement elements.
        """

        market = UsFinancials()
        std_financial = market.get_std_financials(
            ticker=self.ticker,
            which_financial=which_financial,
            period=period,
        )

        return std_financial

    def historical(self, start: Optional[str] = '1900-01-01',
                   end: Optional[str] = None) -> pd.DataFrame:
        """Get historical stock price data.

        Args:
            start: Start date to query. Format should be in ISO 8601.
                e.g. 2021-8-1 or 2021-08-01
                If empty, 1900-01-01 is passed.
            end: End date to query. Format should be in ISO 8601.
                e.g. 2021-8-10 or 2021-08-10
                If empty, date of today is passed.

        Returns:
            Historical stock price data in dataframe.
        """
        price = UsMarket(self.ticker, start, end)
        price_data = price.get_price_data()

        return price_data
