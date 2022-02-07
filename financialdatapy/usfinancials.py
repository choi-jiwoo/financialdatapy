"""This module retrieves financial statements of a company in US."""
import pandas as pd
import webbrowser
from financialdatapy.exception import EmptyDataFrameError
from financialdatapy.filings import get_latest_form
from financialdatapy.filings import get_filings_list
from financialdatapy.request import Request
from financialdatapy.financials import Financials


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
        """Retrieve latest filing that is submitted either 10-K or 10-Q.

        :raises EmptyDataFrameError: Failed getting filing list data.
        :return: Information on latest filing.
        :rtype: pandas.Series
        """
        if self.period == 'annual':
            form_type = '10-K'
        else:
            form_type = '10-Q'

        submission = get_filings_list(self.cik)

        if submission[submission['Form'] == form_type].empty:
            raise EmptyDataFrameError('Failed in getting filings list.')

        form = submission[submission['Form'] == form_type]
        latest_filing = form.iloc[0]

        return latest_filing

    def _get_link_to_latest_filing(self, accession_number: str,
                                   file_name: str) -> str:
        """Get a link to a corporate filing in SEC EDGAR system.

        :param accession_number: Filing identitry number.
        :type accession_number: str
        :param file_name: File name of the filing.
        :type file_name: str
        :return: Link to the filing.
        :rtype: str
        """
        base_url = 'https://www.sec.gov/Archives/edgar/data/'
        link = f'{base_url}/{self.cik}/{accession_number}/{file_name}'

        return link

    def open_report(self) -> None:
        """Open a link of the corporate filing in a web browser."""
        latest_filing = self._get_latest_filing_info()
        accession_number = latest_filing['AccessionNumber']
        file_name = latest_filing['PrimaryDocument']
        report_link = self._get_link_to_latest_filing(accession_number,
                                                      file_name)
        webbrowser.open(report_link, new=0)

    def get_financials(self) -> pd.DataFrame:
        """Get financial statement as reported.

        :return: Financial statement as reported.
        :rtype: pandas.DataFrame
        """
        latest_filing = self._get_latest_filing_info()
        accession_number = latest_filing['AccessionNumber']
        links = get_latest_form(self.cik, accession_number)
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
