"""This module retrieves financial statements of a company in South Korea."""
from datetime import datetime
from functools import lru_cache
from dotenv import load_dotenv
import os
import pandas as pd
from financialdatapy.financials import Financials
from financialdatapy.financials import EmptyDataFrameError
from financialdatapy.request import Request
from financialdatapy.stocklist import StockList


class KorFinancials(Financials):

    load_dotenv()
    API_KEY = os.environ.get('DART_API_KEY')

    def __init__(self, symbol: str, financial: str = 'income_statement',
                 period: str = 'annual') -> None:
        super().__init__(symbol, financial, period)
        self.corp_code = self._get_corp_code()

    def _get_corp_code(self) -> str:
        corp_list = StockList.get_comp_code_list(KorFinancials.API_KEY)
        result = corp_list[corp_list['stock_code'] == self.symbol]
        corp_code = result.get('corp_code').item()

        return corp_code

    @lru_cache
    def _get_latest_report_date(self, year) -> datetime:
        url = 'https://opendart.fss.or.kr/api/list.json'
        last_year = year - 1
        bgn_de = f'{last_year}0101'
        periodical = 'A'
        params = {
            'crtfc_key': KorFinancials.API_KEY,
            'corp_code': self.corp_code,
            'pblntf_ty': periodical,
            'bgn_de': bgn_de,
        }
        res = Request(url, params=params)
        data = res.get_json()
        report_list = pd.DataFrame(data['list'])

        latest_report = data['list'][0]
        latest_date = latest_report['rcept_dt']
        latest_date = datetime.strptime(latest_date, '%Y%m%d')

        return latest_date

    @lru_cache
    def _get_report(self, period, year):
        url = 'https://opendart.fss.or.kr/api/fnlttSinglAcntAll.json'
        report_type = {
            '1q': '11013',
            '2q': '11012',
            '3q': '11014',
            'annual': '11011',
        }
        params = {
            'crtfc_key': KorFinancials.API_KEY,
            'corp_code': self.corp_code,
            'bsns_year': year,
            'reprt_code': report_type[period],
            'fs_div': 'CFS',
        }
        res = Request(url, params=params)
        data = res.get_json()

        return data

    def _get_raw_financial(self, period, year) -> pd.DataFrame:
        data = self._get_report(period, year)
        raw_financial = pd.DataFrame(data['list'])

        return raw_financial

    def _clean_financials(self, raw_financials,
                          report_type, period) -> pd.DataFrame:
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

        return statement

    def get_financials(self) -> pd.DataFrame:
        report_type = {
            'income_statement': 'IS',
            'balance_sheet': 'BS',
            'cash_flow': 'CF',
        }
        today = datetime.now()
        year_now = today.year
        month_now = today.month
        latest_date = self._get_latest_report_date(year_now)
        input_period = self.period

        if input_period == 'annual':
            try:
                raw_financial = self._get_raw_financial(input_period, year_now-1)
            except KeyError:
                raw_financial = self._get_raw_financial(input_period, year_now-2)
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

                raw_financial = self._get_raw_financial(input_period, year_now)
            except KeyError:
                print('공시정보없음')

        financial_statement = self._clean_financials(
                raw_financial, report_type[self.financial], input_period
            )

        return financial_statement

    def get_standard_financials(self) -> pd.DataFrame:
        pass
