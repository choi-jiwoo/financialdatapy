"""This module states abstract class for financial statements."""
from abc import ABC, abstractmethod
from datetime import datetime
import pandas as pd
import string
import webbrowser
from financialdatapy import search
from financialdatapy.exception import EmptyDataFrameError
from financialdatapy.exception import NotAvailable
from financialdatapy.filings import get_latest_form
from financialdatapy.filings import get_filings_list
from financialdatapy.dartapi import OpenDart
from financialdatapy.request import Request
from financialdatapy.stocklist import KorStockList
from financialdatapy.stocklist import UsStockList


class Financials(ABC):
    """Abstract class representing financial statements of a company.

    :param symbol: Symbol of a company.
    :type symbol: str
    :param financial: One of the three financial statement.
        'income_statement' or 'balance_sheet' or 'cash_flow', defaults to
        'income_statement'.
    :type financial: str, optional
    :param period: Either 'annual' or 'quarter', defaults to 'annual'
    :type period: str, optional
    """

    def __init__(self, symbol: str, financial: str = 'income_statement',
                 period: str = 'annual') -> None:
        """Initialize Financials."""
        self.symbol = symbol
        self.financial = financial
        self.period = period

    @property
    def symbol(self) -> str:
        """Getter method of property symbol.

        :return: Symbol of a company.
        :rtype: str
        """
        return self._symbol

    @symbol.setter
    def symbol(self, symbol: str) -> None:
        """Setter method of property symbol.

        :param symbol: Symbol of a company.
        :type symbol: str
        """
        self._symbol = symbol.upper()
    
    @property
    def financial(self) -> str:
        """Getter method of property financial.

        :return: Selected type of financial statement.
        :rtype: str
        """
        return self._financial

    @financial.setter
    def financial(self, financial: str) -> None:
        """Setter method of property financial.

        :param financial: One of the three financial statement.
            'income_statement' or 'balance_sheet' or 'cash_flow', defaults to
            'income_statement'.
        :type financial: str
        """
        self._financial = financial.lower()
    
    @property
    def period(self) -> str:
        """Getter method of property period.

        :return: Selected period of financial statement.
        :rtype: str
        """
        return self._period

    @period.setter
    def period(self, period: str) -> None:
        """Setter method of property period.

        :param period: Either 'annual' or 'quarter', defaults to 'annual'.
        :type period: str
        """
        self._period = period.lower()

    @abstractmethod
    def get_financials(self) -> pd.DataFrame:
        pass

    @abstractmethod
    def open_report(self) -> None:
        pass

    def get_standard_financials(self) -> pd.DataFrame:
        """Get standard financial statements of a company from investing.com.

        :return: Standard financial statement.
        :rtype: pandas.DataFrame
        """

        financials = {
            'income_statement': 'INC',
            'balance_sheet': 'BAL',
            'cash_flow': 'CAS',
        }
        periods = {
            'annual': 'Annual',
            'quarter': 'Interim',
        }
        symbol_search_result = search.Company(self.symbol)
        pair_id = symbol_search_result.search_pair_id()
        report_type = financials[self.financial]
        period = periods[self.period]
        params = {
            'action': 'change_report_type',
            'pair_ID': pair_id,
            'report_type': report_type,
            'period_type': period,
        }
        url = ('https://www.investing.com/instruments/Financials/'
               'changereporttypeajax')
        res = Request(url, params=params)
        data = res.response_data('text')
        financial_statement = self._convert_to_table(data, report_type)

        return financial_statement

    def _convert_to_table(self, data: str, report_type: str) -> pd.DataFrame:
        """Convert HTML text to a clean dataframe.

        :param data: Standard financial statement in HTML text.
        :type data: str
        :return: Standard financial statement.
        :param report_type: INC or BAL or CAS.
        :type report_type: str
        :rtype: pandas.DataFrame
        """

        data_table = pd.read_html(data, index_col=0)[0]

        if report_type == 'CAS':
            data_table = self._convert_table_header(data_table, row_idx=2)
        else:
            data_table = self._convert_table_header(data_table, row_idx=1)

        data_table = data_table.replace(r'-$', '0', regex=True)

        for i in data_table:
            data_table[i] = pd.to_numeric(data_table[i], errors='coerce')

        data_table.dropna(inplace=True)

        values_unit = 1_000_000
        data_table = data_table * values_unit
        ignore_word = ['eps', 'dps']

        for i in data_table.index:
            for word in ignore_word:
                if word in i.lower():
                    data_table.loc[i] /= 1_000_000

        data_table.index.rename(None, inplace=True)

        return data_table

    def _convert_table_header(self, df: pd.DataFrame,
                              row_idx: int) -> pd.DataFrame:
        """Convert date in string to datetime object.

        :param df: Standard financial statement.
        :type df: pd.DataFrame
        :param row_idx: Index number of row containing dates.
        :type row_idx: int
        :return: Standard financial statement with dates as columns.
        :rtype: pd.DataFrame
        """

        table_header = df.iloc[-row_idx:].values[0]
        table_header = [
            element.translate(str.maketrans('', '', string.punctuation))
            for element
            in table_header
        ]
        table_header = pd.to_datetime(table_header, format='%Y%d%m')

        df.columns = table_header
        df = df.iloc[:-row_idx]

        return df


class UsFinancials(Financials):
    """A class representing financial statements of a company in US.

    :param symbol: Symbol of a company.
    :type symbol: str
    :param financial: One of the three financial statement.
        'income_statement' or 'balance_sheet' or 'cash_flow', defaults to
        'income_statement'.
    :type financial: str, optional
    :param period: Either 'annual' or 'quarter', defaults to 'annual'
    :type period: str, optional
    """

    def __init__(self, symbol: str,
                 financial: str = 'income_statement',
                 period: str = 'annual') -> None:
        """Initializes UsFinancials."""
        super().__init__(symbol, financial, period)

    def _get_latest_filing_info(self) -> tuple[str, pd.Series]:
        """Retrieve latest filing that is submitted either 10-K or 10-Q.
        
        :raises EmptyDataFrameError: Failed getting filing list data.
        :return: Cik of a company and Information on the companies latest
            filing.
        :rtype: tuple[str, pandas.Series]
        """
        if self.period == 'annual':
            form_type = '10-K'
        else:
            form_type = '10-Q'

        cik_list = UsStockList()
        cik = cik_list.search_cik(self.symbol)
        submission = get_filings_list(cik)

        if submission[submission['Form'] == form_type].empty:
            raise EmptyDataFrameError('Failed in getting filings list.')

        form = submission[submission['Form'] == form_type]
        latest_filing = form.iloc[0]

        return cik, latest_filing

    def _get_link_to_latest_filing(self, cik: str, accession_number: str,
                                   file_name: str) -> str:
        """Get a link to a corporate filing in SEC EDGAR system.

        :param cik: Cik of a company.
        :type cik: str
        :param accession_number: Filing identitry number.
        :type accession_number: str
        :param file_name: File name of the filing.
        :type file_name: str
        :return: Link to the filing.
        :rtype: str
        """
        base_url = 'https://www.sec.gov/Archives/edgar/data/'
        link = f'{base_url}/{cik}/{accession_number}/{file_name}'

        return link

    def open_report(self) -> None:
        """Open a link of the corporate filing in a web browser."""
        cik, latest_filing = self._get_latest_filing_info()
        accession_number = latest_filing['AccessionNumber']
        file_name = latest_filing['PrimaryDocument']
        report_link = self._get_link_to_latest_filing(cik,
                                                      accession_number,
                                                      file_name)
        webbrowser.open(report_link, new=0)

    def get_financials(self) -> pd.DataFrame:
        """Get financial statement as reported.

        :return: Financial statement as reported.
        :rtype: pandas.DataFrame
        """
        cik, latest_filing = self._get_latest_filing_info()
        accession_number = latest_filing['AccessionNumber']
        links = get_latest_form(cik, accession_number)
        which_financial = links[self.financial]
        financial_statement = self._get_values(which_financial)

        return financial_statement

    def _get_values(self, link: str) -> pd.DataFrame:
        """Extract a financial statement values from web.

        :param link: Url that has financial statment data in a table form.
        :type link: str
        :return: A financial statement.
        :rtype: pandas.DataFrame
        """

        res = Request(link)
        data = res.response_data('text')
        financial_statement = pd.read_html(data)[0]

        first_column = financial_statement.columns[0]
        multi_index = len(first_column)

        if multi_index == 2:
            first_column_header = financial_statement.columns[0][0]
        else:
            first_column_header = financial_statement.columns[0]

        title, unit = first_column_header.split(' - ')
        elements = financial_statement.iloc[:, 0].rename((title, unit))

        financial_statement = financial_statement.drop(
            columns=financial_statement.columns[0]
        )
        financial_statement.insert(
            loc=0,
            column=elements.name,
            value=list(elements.values),
            allow_duplicates=True,
        )

        financial_statement = financial_statement.fillna('')

        financial_statement.iloc[:, 1:] = financial_statement.iloc[:, 1:].apply(
            lambda x: [
                ''.join(filter(str.isdigit, i))
                for i
                in x
            ]
        )

        return financial_statement


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

    def __init__(self, symbol: str, financial: str = 'income_statement',
                 period: str = 'annual') -> None:
        """Initialize KorFinancials"""
        super().__init__(symbol, financial, period)

    def _get_raw_financials(self) -> tuple[pd.DataFrame, str]:
        """Assign period and year according to the user input.

        Pass appropriate parameters for getting financials data in dart system.

        :return: Uncleaned financial statement and assigned input period
        :rtype: tuple[pandas.DataFrame, str]
        """
        kor_stock_list = KorStockList()
        corp_code = kor_stock_list.search_corp_code(self.symbol)
        today = datetime.now()
        year_now = today.year
        open_dart = OpenDart()
        latest_report = open_dart.get_latest_report_info(corp_code, year_now)
        latest_date = latest_report['rcept_dt']
        latest_date = datetime.strptime(latest_date, '%Y%m%d')

        input_period = self.period

        if input_period == 'annual':
            try:
                last_year = year_now - 1
                raw_financial = open_dart.get_report(
                    corp_code,
                    input_period,
                    last_year,
                )
            except KeyError:
                two_yrs_ago = year_now - 2
                raw_financial = open_dart.get_report(
                    corp_code,
                    input_period,
                    two_yrs_ago,
                )
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

                raw_financial = open_dart.get_report(
                    corp_code,
                    input_period,
                    year_now,
                )
            except KeyError:
                raise NotAvailable('Cannot find a report.')

        return raw_financial, input_period

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
