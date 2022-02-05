"""This module retrieves stock lists."""
import pandas as pd
from string import capwords
import re
from financialdatapy import request


class CikList:
    """Class representing cik list of stocks in US exchange."""

    @staticmethod
    def get_cik_list() -> pd.DataFrame:
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
