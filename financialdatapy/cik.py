"""This module retrieves stock lists."""
from string import capwords
from functools import lru_cache
import pandas as pd
import re
from financialdatapy.exception import EmptyDataFrameError
from financialdatapy import request


class CikList:
    """Class representing cik list of stocks in US exchange."""

    @lru_cache
    def get_cik_list(self) -> pd.DataFrame:
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

    def search_cik(self, symbol: str) -> str:
        """Search CIK of specific a company.

        :param symbol: Company symbol to search.
        :type symbol: str
        :return: CIK of the company searching for.
        :rtype: str
        """
        symbol_uppercase = symbol.upper()
        cik_list = self.get_cik_list()
        symbol_df = cik_list[cik_list['ticker'] == symbol_uppercase]
        if symbol_df.empty:
            raise EmptyDataFrameError('Cannot search for the symbol.')
        cik = symbol_df['cik'].item()

        # cik number received from source excludes 0s that comes first.
        # Since cik is a 10-digit number, concatenate 0s.
        zeros = 10 - len(str(cik))
        cik = ('0' * zeros) + str(cik)

        return cik
