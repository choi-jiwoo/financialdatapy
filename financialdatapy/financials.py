"""This module states abstract class for financial statements."""
from abc import ABC, abstractmethod
import pandas as pd
import string
from financialdatapy.request import Request
from financialdatapy import search


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
        self.symbol = symbol.upper()
        self.financial = financial.lower()
        self.period = period.lower()

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
        data = res.get_text()
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
