"""This module retrieves stock lists."""
from abc import ABC, abstractmethod
import pandas as pd
from string import capwords
import re
from financialdatapy import request


class NeedsUpdateError(Exception):
    """Raised if cik list needs to be updated to the latest."""
    pass


class StockList(ABC):

    def template_method(self, update: bool) -> pd.DataFrame:
        """Get stock list data saved in local.

        If it is not saved in local, retrieve the data from source.

        :param update: Updates stock list to the latest.
        :type update: bool
        :return: Stock list.
        :rtype: pandas.DataFrame
        """
        try:
            if update:
                raise NeedsUpdateError()
            usa_stock_list = pd.read_csv('data/usa_stock_list.csv')
        except (FileNotFoundError, NeedsUpdateError):
            usa_stock_list = self.get_data()
            usa_stock_list.to_csv('data/usa_stock_list.csv', index=False)

        return usa_stock_list

    @abstractmethod
    def get_data(self):
        pass


class UsStockList(StockList):

    def get_data(self) -> pd.DataFrame:
        """Get a list of companies CIK(Central Index Key) from SEC.

        The list also contains ticker of a company.

        :return: Dataframe with CIK, company name, and ticker for its columns.
        :rtype: pandas.DataFrame
        """
        url = 'https://www.sec.gov/files/company_tickers_exchange.json'
        res = request.Request(url)
        cik_data = res.get_json()

        cik_list = pd.DataFrame(cik_data['data'], columns=cik_data['fields'])

        cik_list['exchange'] = cik_list['exchange'].str.upper()
        cik_list = cik_list[
            (cik_list['exchange'] == 'NASDAQ') | (cik_list['exchange'] == 'NYSE')
        ]
        cik_list = cik_list.reset_index(drop=True)
        cik_list = cik_list.drop('exchange', axis=1)

        cik_list['cik'] = cik_list['cik'].astype(str)

        # remove all characters after '\' or '/' in a company name
        # ex) Qualcomm inc\de -> Qualcomm inc
        pattern = r'\s?(\/|\\)[a-zA-Z]*'
        regex = re.compile(pattern, flags=re.I)
        cik_list['name'] = [regex.sub('', x) for x in cik_list['name']]

        # comapany names in Title Case
        cik_list['name'] = [capwords(x) for x in cik_list['name']]

        return cik_list


class KorStockList(StockList):
    # to be filled
    def get_data(self) -> pd.DataFrame:
        pass


def get_stock_list(stock_list: StockList, update: bool = False):
    return stock_list.template_method(update)
