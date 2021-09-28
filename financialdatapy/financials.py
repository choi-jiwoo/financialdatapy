"""This module retrieves financial statements of a company."""
from abc import ABC, abstractmethod
import pandas as pd
import json
from financialdatapy import request
from financialdatapy.filings import get_latest_form


class EmptyDataFrameError(Exception):
    """Exception when retreived dataframe is empty."""
    pass


class Financials(ABC):
    """A Class representing financial statements. of a company."""

    @abstractmethod
    def get_financials(self, cik_num: str, submission: pd.DataFrame,
                       form_type: str) -> dict:
        """Get financial statements from either 10-K or 10-Q form.

        :param cik_num: CIK of a company.
        :type cik_num: str
        :param submission: All company filings information.
        :type submission: pandas.DataFrame
        :param form_type: Either 10-K or 10-Q.
        :type form_type: str
        :raises: :class:`EmptyDataFrameError`: If retreived dataframe is empty.
        :return: Dictionary containing each financial statements data.
        :rtype: dict
        """
        pass

    @abstractmethod
    def get_values(self, link: str) -> pd.DataFrame:
        """Extract a financial statement values from web.

        :param link: Url that has financial statment data in a table form.
        :type link: str
        :return: A financial statement.
        :rtype: pandas.DataFrame
        """
        pass

    @abstractmethod
    def get_std_financials(self, ticker: str,
                           which_financial: str,
                           period: str = 'annual') -> pd.DataFrame:
        """Get standard financial statements of a company from finviz.com.

        :param ticker: Ticker of a company.
        :type ticker: str
        :param which_financial: One of the three financial statement.
            'income_statement' or 'balance_sheet' or 'cash_flow', defaults to
            'income_statement'.
        :type which_financial: str
        :param period: Either 'annual' or 'quarter', defaults to 'annual'
        :type period: str, optional
        :return: Standard financial statement.
        :rtype: pandas.DataFrame
        """
        pass


class UsFinancials(Financials):
    """A class representing financial statements of a company in US."""

    def get_financials(self, cik_num: str, submission: pd.DataFrame,
                       form_type: str) -> dict:
        form_type = form_type.upper()

        if submission[submission['Form'] == form_type].empty:
            raise EmptyDataFrameError('Failed in getting financials.')

        # get latest filing
        form = submission[submission['Form'] == form_type]
        latest_filing = form.iloc[0].at['AccessionNumber']
        links = get_latest_form(cik_num, latest_filing)

        is_l = links.get('income_statement')
        income_statement = self.get_values(is_l)

        bs_l = links.get('balance_sheet')
        balance_sheet = self.get_values(bs_l)

        cf_l = links.get('cash_flow')
        cash_flow = self.get_values(cf_l)

        financial_statements = {
            'income_statement': income_statement,
            'balance_sheet': balance_sheet,
            'cash_flow': cash_flow,
        }

        return financial_statements

    def get_values(self, link: str) -> pd.DataFrame:
        res = request.Request(link)
        df = pd.read_html(res.res.text)[0]

        first_column = df.columns[0]
        multi_index = len(first_column)

        if multi_index == 2:
            first_column_header = df.columns[0][0]
        else:
            first_column_header = df.columns[0]

        title, unit = first_column_header.split(' - ')
        new_column_name = df.iloc[:, 0].rename((title, unit))

        df = df.drop(columns=df.columns[0])
        df.insert(
            loc=0,
            column=new_column_name.name,
            value=[*new_column_name.values],
            allow_duplicates=True,
        )

        df = df.fillna('')

        from_element = 1
        df.iloc[:, from_element:] = df.iloc[:, from_element:].apply(
            lambda x: [
                ''.join(filter(str.isdigit, i))
                for i
                in x
            ]
        )

        return df

    def get_std_financials(self, ticker: str,
                           which_financial: str,
                           period: str = 'annual') -> pd.DataFrame:
        financials = {
            'income_statement': 'I',
            'balance_sheet': 'B',
            'cash_flow': 'C',
        }
        periods = {
            'annual': 'A',
            'quarter': 'Q',
        }
        statement = financials[which_financial] + periods[period]
        url = f'https://finviz.com/api/statement.ashx?t={ticker}&s={statement}'
        res = request.Request(url)
        data = res.get_json()

        financial_statement = self.__convert_to_table(data)

        return financial_statement

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

    def __convert_into_korean(self, statement: pd.DataFrame) -> pd.DataFrame:
        """Translate elements of standard financial statements in Korean.

        :param statement: Standard financial statement in English.
        :type statement: pandas.DataFrame
        :return: Standard financial statement in Korean.
        :rtype: pandas.DataFrame
        """
        # elements of financial statements mapped with translations in korean.
        with open('data/statements_kor.json', 'r') as f:
            stmts_in_kor = json.load(f)

        for i in statement.index:
            statement.rename(index={i: stmts_in_kor[i]}, inplace=True)

        return statement
