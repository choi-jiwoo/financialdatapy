"""This module retrieves company code with its company name."""
from financialdatapy.request import Request


class CompanyCode:

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
