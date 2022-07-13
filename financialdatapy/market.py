"""This module handles logic of choosing which stock exchange to search."""
from datetime import datetime
import pandas as pd
from typing import Optional
from financialdatapy.exception import NotAvailable
from financialdatapy.financials import KorFinancials
from financialdatapy.financials import UsFinancials
from financialdatapy.price import UsMarket
from financialdatapy.price import KorMarket


class Market:
    """This class represents a stock exchange.

    :param country_code: Country where the stock is listed.
    :type country_code: str
    """
    def __init__(self, country_code: str) -> None:
        """Initialize Market."""
        self.country_code = country_code

    def financial_statement(
            self,
            symbol: str,
            financial: str,
            period: str,
            is_standard: bool,
            web: bool,
    ) -> Optional[pd.DataFrame]:
        """Get financial statements.

        :param symbol: Symbol of a company/stock.
        :type symbol: str
        :param financial: Which financial statement to retrieve.
        :type financial: str
        :param period: Either 'annual' or 'quarter.
        :type period: str
        :param is_standard: Option for retrieving standard financial statements.
        :type is_standard: bool
        :param web: Option for opening filings in a web browser.
        :type web: bool
        :raises NotAvailable: If the symbol is not listed in the
            stock exchange.
        :return: Financials as reported or standard financials or None.
        :rtype: pandas.DataFrame or None
        """
        match self.country_code:
            case 'USA':
                stock = UsFinancials(symbol, financial, period)
            case 'KOR':
                stock = KorFinancials(symbol, financial, period)
            case _:
                raise NotAvailable('Symbol is not found.')        
        if web:
            stock.open_report()
            return
        if is_standard:
            return stock.get_standard_financials()
        else:
            return stock.get_financials()

    def historical_price(self, symbol: str,
                         start: datetime, end: datetime) -> pd.DataFrame:
        """Get historical stock price data.

        :param symbol: Symbol of a company/stock.
        :type symbol: str
        :param start: Start date to query.
        :type start: `datetime.datetime`
        :param end: End date to query.
        :type end: `datetime.datetime`
        :raises NotAvailable: If the symbol is not listed in the
            stock exchange.
        :return: Historical stock price data.
        :rtype: pandas.DataFrame
        """
        if self.country_code == 'USA':
            return UsMarket(symbol, start, end)
        elif self.country_code == 'KOR':
            return KorMarket(symbol, start, end)
        else:
            raise NotAvailable()
