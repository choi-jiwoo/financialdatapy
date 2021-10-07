import pandas as pd
from financialdatapy.cik import get_stock_list
from financialdatapy.cik import UsStockList


class StockList():
    """Stock list as a class variable.

    :Example:

    >>> from financialdatapy.stocklist import StockList
    >>> us_stock_list = StockList.us_stock_list
    >>> us_stock_list
       cik|       name| ticker
    ------|-----------|-------
    320193| Apple Inc.|   AAPL
    """

    us_stock_list = get_stock_list(UsStockList())

    @staticmethod
    def update_stock_list():
        """Update stock list to the latest.

        :Example:

        >>> from financialdatapy.stocklist import StockList
        >>> StockList.update_stock_list()
        """
        StockList.us_stock_list = get_stock_list(UsStockList(), update=True)

    @staticmethod
    def search_cik(symbol: str) -> str:
        """Search CIK of specific a company.

        :param symbol: Company symbol to search.
        :type symbol: str
        :return: CIK of the company searching for.
        :rtype: str
        """
        symbol = symbol.upper()
        stock_list = StockList.us_stock_list
        symbol_df = stock_list[stock_list['ticker'] == symbol]
        cik = symbol_df['cik'].item()

        # cik number received from source excludes 0s that comes first.
        # Since cik is a 10-digit number, concatenate 0s.
        zeros = 10 - len(str(cik))
        cik = ('0' * zeros) + str(cik)

        return cik
