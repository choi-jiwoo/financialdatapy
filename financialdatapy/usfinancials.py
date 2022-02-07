"""This module retrieves financial statements of a company in US."""
import pandas as pd
import webbrowser
from financialdatapy.filings import get_latest_form
from financialdatapy.filings import get_filings_list
from financialdatapy.request import Request
from financialdatapy.financials import Financials


class EmptyDataFrameError(Exception):
    """Raised when retreived dataframe is empty."""
    pass


class UsFinancials(Financials):
    """A class representing financial statements of a company in US.

    :param symbol: Symbol of a company.
    :type symbol: str
    :param cik: Cik of a company.
    :type cik: str, optional
    :param financial: One of the three financial statement.
        'income_statement' or 'balance_sheet' or 'cash_flow', defaults to
        'income_statement'.
    :type financial: str, optional
    :param period: Either 'annual' or 'quarter', defaults to 'annual'
    :type period: str, optional
    """

    def __init__(self, symbol: str, cik: str,
                 financial: str = 'income_statement',
                 period: str = 'annual') -> None:
        """Initializes UsFinancials."""
        super().__init__(symbol, financial, period)
        self.cik = cik

    def _get_latest_filing_info(self) -> pd.Series:
        if self.period == 'annual':
            form_type = '10-K'
        else:
            form_type = '10-Q'

        submission = get_filings_list(self.cik)

        if submission[submission['Form'] == form_type].empty:
            raise EmptyDataFrameError('Failed in getting financials.')

        form = submission[submission['Form'] == form_type]
        latest_filing = form.iloc[0]

        return latest_filing

    def open_report(self) -> None:
        latest_filing = self._get_latest_filing_info()
        accession_number = latest_filing['AccessionNumber']
        file_name = latest_filing['PrimaryDocument']
        report_link = self._get_link_to_latest_filing(accession_number,
                                                      file_name)
        webbrowser.open(report_link, new=0)

    def get_financials(self) -> pd.DataFrame:
        """Get financial statement as reported.

        :raises EmptyDataFrameError: If retreived dataframe is empty.
        :return: Financial statement as reported.
        :rtype: pandas.DataFrame
        """
        latest_filing = self._get_latest_filing_info()
        accession_number = latest_filing['AccessionNumber']
        links = get_latest_form(self.cik, accession_number)
        which_financial = links[self.financial]
        financial_statement = self._get_values(which_financial)

        return financial_statement

    def _get_link_to_latest_filing(self, accession_number: str,
                                   file_name: str) -> str:
        base_url = 'https://www.sec.gov/Archives/edgar/data/'
        link = f'{base_url}/{self.cik}/{accession_number}/{file_name}'

        return link

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
