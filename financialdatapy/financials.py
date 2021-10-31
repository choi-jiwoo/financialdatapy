"""This module retrieves financial statements of a company."""
from abc import ABC, abstractmethod
import pandas as pd
import json
from typing import Optional
from financialdatapy import request
from financialdatapy.filings import get_latest_form
from financialdatapy.filings import get_filings_list
from financialdatapy import search


class EmptyDataFrameError(Exception):
    """Raised when retreived dataframe is empty."""
    pass


class Financials(ABC):
    """A Class representing financial statements of a company.

    :param cik: Cik of a company.
    :type cik: str, optional
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
                 period: str = 'annual', cik: Optional[str] = None) -> None:
        """Initialize financial statement."""
        self.symbol = symbol.upper()
        self.financial = financial.lower()
        self.period = period.lower()
        self.cik = cik

    @abstractmethod
    def get_financials(self):
        pass

    @abstractmethod
    def get_standard_financials(self):
        pass


class UsFinancials(Financials):
    """A class representing financial statements of a company in US."""

    def get_financials(self) -> pd.DataFrame:
        """Get financial statement as reported.

        :raises: :class:`EmptyDataFrameError`: If retreived dataframe is empty.
        :return: Financial statement as reported.
        :rtype: pandas.DataFrame
        """
        if self.period == 'annual':
            form_type = '10-K'
        else:
            form_type = '10-Q'

        submission = get_filings_list(self.cik)

        if submission[submission['Form'] == form_type].empty:
            raise EmptyDataFrameError('Failed in getting financials.')

        # get latest filing
        form = submission[submission['Form'] == form_type]
        latest_filing = form.iloc[0].at['AccessionNumber']
        links = get_latest_form(self.cik, latest_filing)

        which_financial = links[self.financial]
        financial_statement = self.__get_values(which_financial)

        return financial_statement

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
        pair_id = symbol_search_result.pair_id
        type = financials[self.financial]
        period = periods[self.period]
        url = ('https://www.investing.com/instruments/Financials/'
               'changereporttypeajax?action=change_report_type&'
               f'pair_ID={pair_id}&report_type={type}&period_type={period}')
        res = request.Request(url)
        data = res.get_json()

        financial_statement = self.__convert_to_table(data)

        return financial_statement

    def __get_values(self, link: str) -> pd.DataFrame:
        """Extract a financial statement values from web.

        :param link: Url that has financial statment data in a table form.
        :type link: str
        :return: A financial statement.
        :rtype: pandas.DataFrame
        """
        res = request.Request(link)
        df = pd.read_html(res.res.text)[0]

        first_column = df.columns[0]
        multi_index = len(first_column)

        if multi_index == 2:
            first_column_header = df.columns[0][0]
        else:
            first_column_header = df.columns[0]

        title, unit = first_column_header.split(' - ')
        elements = df.iloc[:, 0].rename((title, unit))

        df = df.drop(columns=df.columns[0])
        df.insert(
            loc=0,
            column=elements.name,
            value=list(elements.values),
            allow_duplicates=True,
        )

        df = df.fillna('')

        df.iloc[:, 1:] = df.iloc[:, 1:].apply(
            lambda x: [
                ''.join(filter(str.isdigit, i))
                for i
                in x
            ]
        )

        return df

    def __convert_to_table(self, data: dict) -> pd.DataFrame:
        """Convert JSON file to a clean dataframe.

        :param data: Standard financial statement in JSON.
        :type data: dict
        :return: Standard financial statement.
        :rtype: pandas.DataFrame
        """
        del data['currency']
        if 'Period Length' in data['data']:
            del data['data']['Period Length']

        df = pd.DataFrame(data['data']).T
        date = df.iloc[0, :].values
        df.columns = date
        row_with_dates = df.index[[0]]
        df.drop(row_with_dates, axis='index', inplace=True)

        df = df.replace(',', '', regex=True)
        for i in df:
            df[i] = pd.to_numeric(df[i])

        values_unit = 1_000_000
        df = df * values_unit

        ignore_word = ['eps', 'employee', 'number']
        for i in df.index:
            for word in ignore_word:
                if word in i.lower():
                    df.loc[i] /= 1_000_000

        return df
