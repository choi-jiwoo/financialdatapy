"""This module retrieves financial statements of a company in South Korea."""
from datetime import datetime
from functools import lru_cache
import pandas as pd
import webbrowser
from financialdatapy.exception import EmptyDataFrameError
from financialdatapy.exception import StatusMessageException
from financialdatapy.financials import Financials
from financialdatapy.request import Request
from financialdatapy.stocklist import KorStockList


class KorFinancials(Financials):
    """Class representing financial statements of stocks in Korea Exchange.

    :param symbol: Symbol of a company/stock.
    :type symbol: str
    :param financial: Which financial statement to retrieve, defaults to
        'income_statement'.
    :type financial: str, optional
    :param period: Either 'annual' or 'quarter', defaults to 'annual'.
    :type period: str, optional
    :param api_key: Api key for opendart.fss.or.kr, defaults to None.
    :type api_key: str
    """

    def __init__(self, symbol: str, api_key: str,
                 financial: str = 'income_statement',
                 period: str = 'annual') -> None:
        """Initialize KorFinancials"""
        super().__init__(symbol, financial, period)
        self.api_key = api_key

    @property
    def corp_code(self) -> str:
        """Get corporate code from dart.fss.or.kr.

        :return: Corporate code.
        :rtype: str
        """
        corp_list = KorStockList(self.api_key).get_stock_list()
        result = corp_list[corp_list['stock_code'] == self.symbol]
        if result.empty:
            raise EmptyDataFrameError('Cannot search for the symbol.')
        corp_code = result.get('corp_code').item()

        return corp_code

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

    @lru_cache
    def _get_latest_report_info(self, year: int) -> datetime:
        """Get the latest date a financial report is submitted to dart.fss.or.kr

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
            'corp_code': self.corp_code,
            'pblntf_ty': periodical,
            'bgn_de': bgn_de,
        }
        res = Request(url, params=params)
        data = res.get_json()
        self._validate_status(data)
        report_list = pd.DataFrame(data['list'])

        latest_report = data['list'][0]

        return latest_report

    def _get_report(self, period: str, year: int) -> pd.DataFrame:
        """Retrieve financial statement of a company from dart.fss.or.kr.

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
            'corp_code': self.corp_code,
            'bsns_year': year,
            'reprt_code': report_type[period],
            'fs_div': 'CFS',
        }
        res = Request(url, params=params)
        data = res.get_json()
        raw_financial = pd.DataFrame(data['list'])
        self._validate_status(data)

        return raw_financial

    def _clean_financials(self, raw_financials: pd.DataFrame,
                          report_type: str, period: str) -> pd.DataFrame:
        """Clean financial statement retrieved from dart.fss.or.kr.

        :param raw_financials: Financial statement.
        :type raw_financials: pandas.DataFrame
        :param report_type: Which financial statement.
        :type report_type: str
        :param period: Either 'annual' or 'quarter'.
        :type period: str
        :return: Financial statement of a company.
        :rtype: pandas.DataFrame
        """
        statement = raw_financials[raw_financials['sj_div'] == report_type]

        if period == 'annual':
            cols = statement.iloc[0, :].get(
                [
                    'sj_nm',
                    'thstrm_nm',
                    'frmtrm_nm',
                    'bfefrmtrm_nm',
                ]
            ).to_numpy()
            statement = statement.get(
                [
                    'account_nm',
                    'thstrm_amount',
                    'frmtrm_amount',
                    'bfefrmtrm_amount',
                ]
            )
        else:
            cols = statement.iloc[0, :].get(
                [
                    'sj_nm',
                    'thstrm_nm'
                ]
            ).to_numpy()
            statement = statement.get(
                [
                    'account_nm',
                    'thstrm_amount'
                ]
            )

        statement.columns = cols
        statement.reset_index(drop=True, inplace=True)

        return statement

    def _get_raw_financials(self) -> tuple[pd.DataFrame, str]:
        """Assign period and year according to the user input.

        Pass appropriate parameters for getting financials data in dart system.

        :return: Uncleaned financial statement and assigned input period
        :rtype: tuple[pandas.DataFrame, str]
        """
        today = datetime.now()
        year_now = today.year
        month_now = today.month
        latest_report = self._get_latest_report_info(year_now)
        latest_date = latest_report['rcept_dt']
        latest_date = datetime.strptime(latest_date, '%Y%m%d')

        input_period = self.period

        if input_period == 'annual':
            try:
                raw_financial = self._get_report(input_period, year_now - 1)
            except KeyError:
                raw_financial = self._get_report(input_period, year_now - 2)
        elif input_period == 'quarter':
            latest_q = latest_date.month
            try:
                if 4 <= latest_q <= 6:
                    input_period = '1q'
                elif 7 <= latest_q <= 9:
                    input_period = '2q'
                else:
                    year_now = year_now - 1
                    input_period = '3q'

                raw_financial = self._get_report(input_period, year_now)
            except KeyError:
                print('공시정보없음')

        return raw_financial, input_period

    def get_financials(self) -> pd.DataFrame:
        """Get financial statement of a company.

        :return: Financial statement.
        :rtype: pandas.DataFrame
        """
        report_type = {
            'income_statement': 'IS',
            'balance_sheet': 'BS',
            'cash_flow': 'CF',
        }
        raw_financial, period = self._get_raw_financials()
        financial_statement = self._clean_financials(
            raw_financial, report_type[self.financial], period
        )

        return financial_statement

    def open_report(self) -> None:
        """Open a link of the corporate filing in a web browser."""
        raw_financial, period = self._get_raw_financials()
        rcept_no = raw_financial['rcept_no'].iloc[0]
        link = f'https://dart.fss.or.kr/dsaf001/main.do?rcpNo={rcept_no}'
        webbrowser.open(link)
