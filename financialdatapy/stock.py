"""Retrieve data of a certain stock.

Scrape data from 3 major financial statements as reported in the SEC EDGAR
system, 3 major standard financial statements from finviz.com,
and a historical price data of a stock (company).

Classes:
    Cik
    Stock

Get a list of CIK:

    from financialdatapy.stock import Cik

    cik_list = Cik.cik_list

Get financial statements:

    from financialdatapy.stock import Stock

    comp = Stock('AAPL')
    fs = comp.financials('10-K')
    std_fs_ic = comp.standard_financials('income_statement', 'annual')

Get historical price data:

    from financialdatapy.stock import Stock

    comp = Stock('AAPL')
    price = comp.historical('2021-1-1', '2021-2-1')
"""
import pandas as pd
import financialdatapy


class Cik():
    """Get cik list as a class variable."""

    cik_list = financialdatapy.get_cik()


class Stock(Cik):
    """Class representing a stock or a company.

    Attributes:
        ticker: Ticker of a stock.

    Methods:
        read_financials(form :str) -> dict:
            Get financial statements as reported.
        read_std_financials(which_financial, period="annual") -> pd.DataFrame:
            Get standard financial statements.

    """

    def __init__(self, ticker: str) -> None:
        """Initialize ticker to search.

        Args:
            ticker: Ticker of a stock.
        """

        self.ticker = ticker.upper()

    def financials(self, form: str = '10-K') -> dict:
        """Get financial statements as reported.

        Args:
            form: Either '10-K' or '10-Q' form. Default value is '10-K'.

        Returns:
            Dictionary with key for the financial statment name
            and value for the actual data.

            Looks like::

                {
                    'income_statement': {...},
                    'balance_sheet': {...},
                    'cash_flow': {...}
                }

        Raises:
            EmptyDataFrameError: If dataframe is empty.
            ImbalanceNumberOfFactsError: When the number of elements and values
                are different.
        """

        comp_cik = financialdatapy.search_cik(Stock.cik_list, self.ticker)
        submission = financialdatapy.get_filings_list(comp_cik)
        name = ['income_statement', 'balance_sheet', 'cash_flow']
        financial_statement = financialdatapy.get_financials(
            comp_cik,
            submission,
            form,
        )
        financial_statement = {
            name[i]: x for i, x in enumerate(financial_statement)
        }
        return financial_statement

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

        std_financial = financialdatapy.get_std_financials(
            ticker=self.ticker,
            which_financial=which_financial,
            period=period,
        )
        return std_financial

    def historical(self, start: str, end: str()) -> dict:
        """Get historical stock price data from finance.yahoo.com.

        Args:
            start: Start date to query. Format should be in ISO 8601.
                e.g. 2021-8-1 or 2021-08-01
            end: End date to query. Format should be in ISO 8601.
                e.g. 2021-8-10 or 2021-08-10

        Returns:
            Historical price data in JSON format.
        """
        ticker = self.ticker
        price = financialdatapy.Price(ticker, start, end)
        price_data = price.get_price_data()
        return price_data
