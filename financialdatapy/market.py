"""This module handles logic of choosing which stock exchange to search."""
from datetime import datetime
import pandas as pd
from typing import Optional
from financialdatapy.dartapi import Dart
from financialdatapy.stocklist import UsStockList
from financialdatapy.exception import NotAvailable
from financialdatapy.korfinancials import KorFinancials
from financialdatapy.usfinancials import UsFinancials
from financialdatapy.price import UsMarket
from financialdatapy.price import KorMarket


class Market:
    """This class represents a stock exchange.

    :param country_code: Country where the stock is listed.
    :type country_code: str
    """

    def __init__(self, country_code: str):
        """Initialize Market."""
        self.country_code = country_code.upper()

    def financial_statement(
            self,
            symbol: str,
            financial: str,
            period: str,
            web: bool = False,
            type_of_financial: Optional[str] = None,
    ) -> pd.DataFrame:
        """Get financial statements.

        :param symbol: Symbol of a company/stock.
        :type symbol: str
        :param financial: Which financial statement to retrieve.
        :type financial: str
        :param period: Either 'annual' or 'quarter.
        :type period: str
        :param web: Option for opening filings in a web browser, defaults to
            False.
        :type web: bool, optional
        :param type_of_financial: Pass 'standard' for the method to return
            standard financials. If empty, finanicials as reported will be
            returned, defaults to None.
        :type type_of_financial: Optional[str], optional
        :raises NotAvailable: If the symbol is not listed in the
            stock exchange.
        :return: Either financials as reported or standard financials.
        :rtype: pandas.DataFrame
        """
        match self.country_code:
            case 'USA':
                cik_list = UsStockList()
                comp_cik = cik_list.search(symbol)
                market = UsFinancials(symbol, comp_cik, financial, period)
            case 'KOR':
                dart = Dart()
                api_key = dart.api_key
                market = KorFinancials(symbol, api_key, financial, period)
            case _:
                raise NotAvailable()

        if web:
            market.open_report()
        else:
            if type_of_financial == 'standard':
                return market.get_standard_financials()
            else:
                return market.get_financials()

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
