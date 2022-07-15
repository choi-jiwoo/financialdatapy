"""This module calls api key stored in .env file."""
from datetime import datetime
from dotenv import load_dotenv
import os
import pandas as pd
from typing import Optional
from financialdatapy.exception import EmptyApiKeyException
from financialdatapy.exception import StatusMessageException
from financialdatapy.request import Request


class DartApiKey:
    """This class represents api key from opendart.fss.or.kr.

    :param api_key: Api key from opendart.fss.or.kr, defaults to None.
    :type api_key: Optional[str], optional
    """

    def __init__(self, api_key: Optional[str] = None) -> None:
        """Initialize Dart."""
        self.api_key = api_key

    @property
    def api_key(self) -> str:
        """Getter method of property api_key.

        :return: Api key from opendart.fss.or.kr
        :rtype: str
        """
        return self._api_key

    @api_key.setter
    def api_key(self, api_key: Optional[str] = None) -> None:
        """Setter method of property api_key.

        :param api_key: Api key from opendart.fss.or.kr, defaults to None.
        :type api_key: Optional[str], optional
        :raises EmptyApiKeyException: Api key is not submitted.
        """
        if api_key is None:
            load_dotenv()
            env_api_key = os.environ.get('DART_API_KEY')
            if env_api_key is None:
                raise EmptyApiKeyException('Dart api key is not provided.')
            self._api_key = env_api_key
        else:
            self._api_key = api_key

class OpenDart(DartApiKey):
    """This class represents OPEN DART API.

    :param api_key: Api key for opendart.fss.or.kr, defaults to None.
    :type api_key: str, optional
    """
    def __init__(self) -> None:
        """Initialize OpenDart."""
        super().__init__()

    def _validate_status(self, data: dict) -> None:
        """Validate if data is successfully retrieved.

        :param data: Response object received.
        :type data: dict
        :raises StatusMessageException: Failed in getting requested data.
        """
        response_status = data['status']
        if response_status != '000':
            status_message = data['message']
            raise StatusMessageException(status_message)

    def get_corp_code_file(self) -> bytes:
        """Get the list of corporate code of a company listed in Korea Exchange.

        Endpoint returns the list in XML file.

        :return: XML file that contains the list of corporate code of a company.
        :rtype: bytes
        """
        url = 'https://opendart.fss.or.kr/api/corpCode.xml'
        params = {
            'crtfc_key': self.api_key
        }
        res = Request(url, params=params)
        corp_code_file = res.response_data('content')
        return corp_code_file

    def get_latest_report_info(self, corp_code: str, year: int) -> datetime:
        """Get the latest date a financial report is submitted to dart.fss.or.kr

        :param corp_code: Corporate code of a company.
        :type corp_code: str
        :param year: Current year.
        :type year: int
        :return: Latest date a financial report is submitted.
        :rtype: `datetime.datetime`
        """
        url = 'https://opendart.fss.or.kr/api/list.json'
        last_year = year - 1
        bgn_de = f'{last_year}0101'
        periodical = 'A'
        params = {
            'crtfc_key': self.api_key,
            'corp_code': corp_code,
            'pblntf_ty': periodical,
            'bgn_de': bgn_de,
        }
        res = Request(url, params=params)
        report_list = res.response_data('json')
        self._validate_status(report_list)
        report_list = pd.Series(report_list['list'])
        latest_report = report_list[0]
        return latest_report

    def get_report(self, corp_code: str, period: str, year: int) -> pd.DataFrame:
        """Retrieve financial statement of a company from dart.fss.or.kr.

        :param corp_code: Corporate code of a company.
        :type corp_code: str
        :param period: Either 'annual' or 'quarter'.
        :type period: str
        :param year: Business year.
        :type year: int
        :return: Financial statement of a company.
        :rtype: pandas.DataFrame
        """
        url = 'https://opendart.fss.or.kr/api/fnlttSinglAcntAll.json'
        report_type = {
            '1q': '11013',
            '2q': '11012',
            '3q': '11014',
            'annual': '11011',
        }
        params = {
            'crtfc_key': self.api_key,
            'corp_code': corp_code,
            'bsns_year': year,
            'reprt_code': report_type[period],
            'fs_div': 'CFS',
        }
        res = Request(url, params=params)
        report = res.response_data('json')
        self._validate_status(report)
        raw_financial = pd.DataFrame(report['list'])
        return raw_financial
