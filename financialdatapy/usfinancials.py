"""This module retrieves financial statements of a company in US."""
import pandas as pd
from financialdatapy.filings import get_latest_form
from financialdatapy.filings import get_filings_list
from financialdatapy.request import Request
from financialdatapy.financials import Financials


class EmptyDataFrameError(Exception):
    """Raised when retreived dataframe is empty."""
    pass


class UsFinancials(Financials):
    """A class representing financial statements of a company in US."""

    def __init__(self, symbol: str, cik: str,
                 financial: str = 'income_statement',
                 period: str = 'annual') -> None:
        super().__init__(symbol, financial, period)
        self.cik = cik

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

    def _get_values(self, link: str) -> pd.DataFrame:
        """Extract a financial statement values from web.

        :param link: Url that has financial statment data in a table form.
        :type link: str
        :return: A financial statement.
        :rtype: pandas.DataFrame
        """

        res = Request(link)
        data = res.get_text()
        df = pd.read_html(data)[0]

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
