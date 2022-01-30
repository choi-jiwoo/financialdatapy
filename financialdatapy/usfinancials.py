"""This module retrieves financial statements of a company in US."""
import pandas as pd
import string
from financialdatapy.filings import get_latest_form
from financialdatapy.filings import get_filings_list
from financialdatapy import search
from financialdatapy.financials import Financials
from financialdatapy.financials import EmptyDataFrameError


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
        financial_statement = self._get_values(which_financial)

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

    def _get_values(self, link: str) -> pd.DataFrame:
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
