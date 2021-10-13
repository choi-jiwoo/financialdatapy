"""This module retrieves stock lists."""
from abc import ABC, abstractmethod
import pandas as pd
from pathlib import Path
from string import capwords
import re
from financialdatapy import request

#: Root directory of a package.
PATH = str(Path(__file__).parents[1]) + '/'


class NeedsUpdateError(Exception):
    """Raised if cik list needs to be updated to the latest."""
    pass


class StockList(ABC):
    """A class representing stock list of listed companies."""

    def template_method(self, update: bool) -> pd.DataFrame:
        """Get stock list data saved in local.

        If it is not saved in local, retrieve the data from source.

        :param update: Updates stock list to the latest.
        :type update: bool
        :raises: :class:`NeedsUpdateError`: If cik list needs to be updated
            to the latest.
        :return: Stock list.
        :rtype: pandas.DataFrame
        """
        try:
            if update:
                raise NeedsUpdateError()
            usa_stock_list = pd.read_csv(PATH+'data/usa_stock_list.csv')
        except (FileNotFoundError, NeedsUpdateError):
            usa_stock_list = self.get_data()
            usa_stock_list.to_csv(PATH+'data/usa_stock_list.csv', index=False)

        return usa_stock_list

    @abstractmethod
    def get_data(self):
        pass


class UsStockList(StockList):
    """A class representing stock list of listed companies in USA."""

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


def get_stock_list(stock_list: StockList, update: bool = False) -> pd.DataFrame:
    """Call StockList.template_method to get stock list data.

    :param stock_list: :class:`StockList` object.
    :type stock_list: StockList
    :param update: Updates stock list to the latest., defaults to False
    :type update: bool, optional
    :return: Stock list.
    :rtype: pandas.DataFrame
    """
    return stock_list.template_method(update)
