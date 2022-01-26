"""This module retrieves stock lists."""
import pandas as pd
from financialdatapy.cik import UsCikList


class StockList():
    """A class representing stock list of listed companies.

    :cvar us_cik_list: Stock list of stocks in the USA.
    :vartype us_cik_list: pandas.DataFrame

    :Example:

    >>> from financialdatapy.stocklist import StockList
    >>> us_cik_list = StockList.us_cik_list
    >>> us_cik_list

    Output::

        |    cik |       name | ticker |
        |--------|------------|--------|
        | 320193 | Apple Inc. |   AAPL |
        |    ... |        ... |    ... |

    """

    @staticmethod
    def update_stock_list():
        """Update stock list to the latest.

        :Example:

        >>> from financialdatapy.stocklist import StockList
        >>> StockList.update_stock_list()
        """
    us_cik_list = UsCikList.get_cik_list()

    @staticmethod
    def search_cik(symbol: str) -> str:
        """Search CIK of specific a company.

        :param symbol: Company symbol to search.
        :type symbol: str
        :return: CIK of the company searching for.
        :rtype: str
        """

        symbol = symbol.upper()
        cik_list = StockList.us_cik_list
        symbol_df = cik_list[cik_list['ticker'] == symbol]
        cik = symbol_df['cik'].item()

        # cik number received from source excludes 0s that comes first.
        # Since cik is a 10-digit number, concatenate 0s.
        zeros = 10 - len(str(cik))
        cik = ('0' * zeros) + str(cik)

        return cik
