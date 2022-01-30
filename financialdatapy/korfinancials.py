"""This module retrieves financial statements of a company in South Korea."""
from datetime import datetime
import pandas as pd
from financialdatapy.financials import Financials
from financialdatapy.financials import EmptyDataFrameError
from financialdatapy.request import Request
from financialdatapy.stocklist import StockList


class KorFinancials(Financials):

    load_dotenv()
    API_KEY = os.environ.get('DART_API_KEY')

    def _get_corp_code(self) -> str:
        corp_list = StockList.get_comp_code_list(KorFinancials.API_KEY)
        result = corp_list[corp_list['stock_code'] == self.symbol]
        corp_code = result.get('corp_code').item()

        return corp_code

    def get_financials(self) -> pd.DataFrame:
        url = 'https://opendart.fss.or.kr/api/fnlttSinglAcntAll.json'
        corp_code = self._get_corp_code()
        report_type = {
            '1q': '11013',
            '2q': '11012',
            '3q': '11014',
            'annual': '11011',
        }
        if self.period == 'annual':
            year = datetime.now().year - 1
        else:
            year = datetime.now().year
        reprt_code = report_type[self.period]
        params = {
            'crtfc_key': KorFinancials.API_KEY,
            'corp_code': corp_code,
            'bsns_year': year,
            'reprt_code': reprt_code,
            'fs_div': 'CFS',
        }

        if self.period == 'annual':
            params['reprt_code'] = report_type[self.period]
            statement = self.get_annual_financials(url, params)

    def get_annual_financials(self, url, params) -> pd.DataFrame:
        financials = {
            'income_statement': 'IS',
            'balance_sheet': 'BS',
            'cash_flow': 'CF',
        }

        res = requests.get(url, params=params)
        data = res.json()

        try:
            raw_financials = pd.DataFrame(data['list'])
        except KeyError:
            print(data['message`'])

        statement = clean_financials(raw_financials,
                                     financials[self.financial])

        return statement

    def clean_financials(self, raw_financials,
                         report_type, period) -> pd.DataFrame:
        statement = raw_financials[raw_financials['sj_div'] == report_type]

        if period == 'annual':
            cols = statement.iloc[0, :].get(['sj_nm', 'thstrm_nm', 'frmtrm_nm', 'bfefrmtrm_nm']).to_numpy()
            statement = statement.get(['account_nm', 'thstrm_amount', 'frmtrm_amount', 'bfefrmtrm_amount'])
        else:
            cols = statement.iloc[0,:].get(['sj_nm', 'thstrm_nm']).to_numpy()
            statement = statement.get(['account_nm', 'thstrm_amount'])

        statement.columns = cols

        return statement

    def get_standard_financials(self) -> pd.DataFrame:
        pass
