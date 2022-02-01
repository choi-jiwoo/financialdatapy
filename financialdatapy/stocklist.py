"""This module retrieves stock lists."""
from io import BytesIO
import json
from functools import lru_cache
import pandas as pd
import xmltodict
from zipfile import ZipFile
from financialdatapy.request import Request
from financialdatapy.cik import UsCikList


class StockList:
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

    @staticmethod
    @lru_cache
    def get_comp_code_list(api_key: str) -> str:
        url = 'https://opendart.fss.or.kr/api/corpCode.xml'
        params = {
            'crtfc_key': api_key
        }
        res = Request(url, params=params)
        zip_file = res.get_content()
        try:
            xml_zip_file = ZipFile(BytesIO(zip_file))
            xml_file = xml_zip_file.read('CORPCODE.xml').decode('utf-8')
            raw_corp_code = xmltodict.parse(xml_file)
            encoded_corp_code = json.dumps(raw_corp_code)
            corp_code = json.loads(encoded_corp_code)

            corp_code_list = pd.DataFrame(corp_code['result']['list'])
            corp_code_list.dropna(inplace=True)

            return corp_code_list
        except Exception as e:
            print(e)
