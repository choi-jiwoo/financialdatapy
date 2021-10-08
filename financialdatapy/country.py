# should add docstring
from typing import Optional
from financialdatapy.financials import UsFinancials
from financialdatapy.price import UsMarket
from financialdatapy.stocklist import StockList


class NotAvailable(Exception):
    def __init__(self, msg: str = 'Data is not available.', *args, **kwargs):
        super().__init__(msg, *args, **kwargs)


class Market:

    def __init__(self, country_code: str):
        self.country_code = country_code

    def financial_statement(self, symbol: str, financial: str, period: str,
                            type_of_financial: Optional[str] = None):
        if self.country_code == 'USA':
            comp_cik = StockList.search_cik(symbol)
            market = UsFinancials(symbol, financial, period, comp_cik)

            if type_of_financial == 'standard':
                return market.get_standard_financials()

            return market.get_financials()
        else:
            raise NotAvailable()

    def historical_price(self, symbol, start, end):
        if self.country_code == 'USA':
            return UsMarket(symbol, start, end)
        else:
            raise NotAvailable()
