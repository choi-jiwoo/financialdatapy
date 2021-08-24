"""Retrieve data of a certain stock.

Scrape data from 3 major financial statements as reported in the SEC EDGAR
system, and 3 major standard financial statements from finviz.com of a
stock (company).

Classes:

    Stock

Usage example:

comp = Stock('AAPL')
fs = comp.read_financials('10-K')
std_fs_ic = comp.read_std_financials('income_statement', 'annual')
"""
import pandas as pd
from scripts import cik
from scripts import filings
from scripts import financials


CIK_LIST = cik.get_cik()


class Stock():
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

        self.ticker = ticker

    def read_financials(self, form: str) -> dict:
        """Get financial statements as reported.

        Args:
            form: Either 10-K or 10-Q form.

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

        comp_cik = cik.search_cik(CIK_LIST, self.ticker)
        submission = filings.get_filings_list(comp_cik)
        name = ['income_statement', 'balance_sheet', 'cash_flow']
        financial_statement = filings.get_financials(
            comp_cik,
            submission,
            form,
        )
        financial_statement = {
            name[i]: x for i, x in enumerate(financial_statement)
        }
        return financial_statement

    def read_std_financials(self, which_financial: str,
                            period: str = 'annual') -> pd.DataFrame:
        """Get standard financial statements.

        Args:
            which_financial: One of the three financial statement.
                'income_statement' or 'balance_sheet' or 'cash_flow'.
            period: Either 'annual' or 'quarter'.

        Returns:
            Dataframe with columns as dates, and index as financial
            statement elements.
        """

        std_financial = financials.get_std_financials(
            ticker=self.ticker,
            which_financial=which_financial,
            period=period,
        )
        return std_financial
