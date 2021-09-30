"""This module retrieves financial data of a stock."""
import pandas as pd
from typing import Optional
from financialdatapy.cik import get_cik_list
from financialdatapy.cik import search_cik
from financialdatapy.filings import get_filings_list
from financialdatapy.financials import UsFinancials
from financialdatapy.price import UsMarket


class Cik():
    """Cik list as a class variable.

    :Example:

    >>> from financialdatapy.stock import Cik
    >>> cik_list = Cik.cik_list
    >>> cik_list
       cik|       name| ticker
    ------|-----------|-------
    320193| Apple Inc.|   AAPL
    """

    #: Get the list of cik of companies registered in SEC.
    cik_list = get_cik_list()

    @staticmethod
    def update_cik_list():
        """Update cik list from SEC to the latest.

        :Example:

        >>> from financialdatapy.stock import Cik
        >>> Cik.update_cik_list()
        """
        Cik.cik_list = get_cik_list(update=True)


class Stock(Cik):
    """A class representing a stock or a company.

    :param ticker: Ticker of a company/stock.
    :type ticker: str
    """

    def __init__(self, ticker: str) -> None:
        """Initialize ticker to search."""
        self.ticker = ticker
        self.comp_cik = search_cik(Stock.cik_list, ticker)

    def financials(self, financial: str = 'income_statement',
                   period: str = 'annual') -> pd.DataFrame:
        """Get financial statements as reported.

        :param financial: Which financial statement to retrieve. Input string
                should be either 'income_statement', 'balance_sheet', or
                'cash_flow', defaults to 'income_statement'
        :type financial: str, optional
        :param period: Either 'annual' or 'quarter, defaults to 'annual'.
        :type period: str, optional
        :return: A dataframe containing financial statement as reported.
        :rtype: pandas.DataFrame

        :Example:

        >>> from financialdatapy.stock import Stock
        >>> comp = Stock('AAPL')
        >>> ic_as_reported = comp.financials('income_statement', 'annual')
        >>> ic_as_reported
             CONSOLIDATED STATEMENTS OF OPERATIONS| 12 Months Ended
        USD ($) shares in Thousands, $ in Millions|   Sep. 26, 2020| Sep. 28, 2019| Sep. 29, 2018
        ------------------------------------------|----------------|--------------|--------------
                                         Net sales|          274515|        260174|        265595
        """
        market = UsFinancials(self.comp_cik, self.ticker, financial, period)
        financial_statement = market.get_financials()

        return financial_statement

    def standard_financials(self, financial: str = 'income_statement',
                            period: str = 'annual') -> pd.DataFrame:
        """Get standard financial statements.

        :param financial: One of the three financial statement.
            'income_statement' or 'balance_sheet' or 'cash_flow', defaults to
            'income_statement'.
        :type financial: str, optional
        :param period: Either 'annual' or 'quarter', defaults to 'annual'.
        :type period: str, optional
        :return: Standard financial statement.
        :rtype: pandas.DataFrame

        :Example:

        >>> from financialdatapy.stock import Stock
        >>> comp = Stock('AAPL')
        >>> std_ic = comp.standard_financials('income_statement', 'annual')
        >>> std_ic
                     |          TTM|    9/26/2020| ...
        -------------|-------------|-------------|----
        Total Revenue| 3.471550e+11| 2.745150e+11| ...
        """
        market = UsFinancials(self.comp_cik, self.ticker, financial, period)
        std_financial = market.get_standard_financials()

        return std_financial

    def historical(self, start: str = '1900-01-01',
                   end: Optional[str] = None) -> pd.DataFrame:
        """Get historical stock price data.

        :param start: Start date to query. Format should be in ISO 8601,
            defaults to 1900-01-01.
        :type start: str, optional
        :param end: End date to query. Format should be in ISO 8601, defaults to
            the date of today.
        :type end: str, optional
        :return: Historical stock price data in dataframe.
        :rtype: pandas.DataFrame

        :Example:

        >>> from financialdatapy.stock import Stock
        >>> comp = Stock('AAPL')
        >>> price = comp.historical('2021-1-1', '2021-1-5')
        >>> price
                  |  close|   open|   high|    low|    volume
        ----------|-------|-------|-------|-------|----------
        2021-01-04| 129.41| 133.52| 133.61| 126.76| 143301900
        """
        price = UsMarket(self.ticker, start, end)
        price_data = price.get_price_data()

        return price_data
