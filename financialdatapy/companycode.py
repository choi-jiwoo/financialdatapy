"""This module retrieves company code with its company name."""
from io import BytesIO
import json
from functools import lru_cache
import pandas as pd
import xmltodict
from zipfile import ZipFile
from financialdatapy.request import Request


class CompanyCode:
    """This class represents company code of a company."""

    @staticmethod
    @lru_cache
    def get_comp_code_list(api_key: str) -> pd.DataFrame:
        """Retrieve company code list of stocks listed in Korea Exchange.

        :param api_key: Api key for opendart.fss.or.kr
        :type api_key: str
        :return: List of company codes.
        :rtype: pandas.DataFrame
        """
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
            raise RuntimeError(e)

    @staticmethod
    def search_code(name: str) -> str:
        """Search company code with company name in dart.fss.or.kr.

        :param name: Company name.
        :type name: str
        :return: Company code.
        :rtype: str
        """
        url = 'https://kind.krx.co.kr/common/searchcorpname.do'
        data = {
            'method': 'searchCorpNameJson',
            'searchCodeType': 'char',
            'searchCorpName': name,
        }
        headers = {
            'User-Agent': 'Mozilla',
            'X-Requested-With': 'XMLHttpRequest',
            'Content-Type': 'application/x-www-form-urlencoded'
        }
        res = Request(url, method='post', headers=headers, data=data)
        comp_info_first_result = res.get_json()[0]
        company_code = comp_info_first_result['repisusrtcd2']

        return company_code
