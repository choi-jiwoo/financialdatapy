"""This module retrieves financial data of a stock."""
import pandas as pd
import re
from typing import Optional
from financialdatapy.country import Market


class CountryCodeValidationFailed(Exception):
    """Raised when country code is not in alpha-3 code format."""
    pass


class Stock():
    """A class representing a stock or a company.

    :param symbol: Symbol of a company/stock.
    :type symbol: str
    :param country_code: Country where the stock is listed. The format should
        follow alpha-3 code (ISO 3166), defaults to 'USA'.
    :type country_code: str, optional
    """

    def __init__(self, symbol: str, country_code: str = 'USA') -> None:
        """Initialize symbol to search."""
        self.symbol = symbol
        self.country_code = self.__validate_country_code(country_code)
        self.market = Market(self.country_code)

    def __validate_country_code(self, country_code: str) -> str:
        """Validate if country code is in alpha-3 code (ISO 3166).

        :param country_code: Country where the stock is listed.
        :type country_code: str
        :raises: :class:`CountryCodeValidationFailed`: If country code is not
            in alpha-3 code format.
        :return: Country code in alpha-3 code (ISO-3166).
        :rtype: str
        """
        try:
            country_code = re.search(r'\b[a-zA-Z]{3}\b', country_code).group()
            country_code = country_code.upper()
        except (TypeError, AttributeError):
            raise CountryCodeValidationFailed(
                'Country code should be in alpha-3 code (ISO 3166) e.g. USA'
            ) from None
        else:
            return country_code

    def financials(self, financial: str = 'income_statement',
                   period: str = 'annual') -> pd.DataFrame:
        """Get financial statements as reported.

        :param financial: Which financial statement to retrieve. Input string
                should be either 'income_statement', 'balance_sheet', or
                'cash_flow', defaults to 'income_statement'
        :type financial: str, optional
        :param period: Either 'annual' or 'quarter, defaults to 'annual'.
        :type period: str, optional
        :return: Financial statement as reported.
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
        return self.market.financial_statement(self.symbol, financial, period)

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
        return self.market.financial_statement(self.symbol, financial,
                                               period, 'standard')

    def historical(self, start: str = '1900-01-01',
                   end: Optional[str] = None) -> pd.DataFrame:
        """Get historical stock price data.

        :param start: Start date to query. Format should be in ISO 8601,
            defaults to 1900-01-01.
        :type start: str, optional
        :param end: End date to query. Format should be in ISO 8601, defaults to
            the date of today.
        :type end: str, optional
        :return: Historical stock price data.
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
        price = self.market.historical_price(self.symbol, start, end)
        price_data = price.get_price_data()

        return price_data
