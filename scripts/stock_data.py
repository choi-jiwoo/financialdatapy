import pandas as pd
from scripts import cik
from scripts import filings
from scripts import financials


CIK_LIST = cik.get_cik()


class Stock():
    def __init__(self, ticker: str) -> None:
        """Initialize ticker to search.

        Args:
            ticker: Ticker of a company.
        """

        self.ticker = ticker

    def get_financials(self, form: str) -> dict:
        """Get 3 major financial statements as reported in SEC EDGAR system.

        Args:
            form: Either 10-K or 10-Q form.

        Returns:
            Dictionary with key for the financial statment name
            and value for the actual data.

            Looks like::

                {
                    'income_statement': {...},
                    'balance_sheet': {...},
                    'cash_flow': {...}
                }

        Raises:
            EmptyDataFrameError: If dataframe is empty.
            ImbalanceNumberOfFactsError: When the number of elements and values
                are different.
        """

        comp_cik = cik.search_cik(CIK_LIST, self.ticker)
        submission = filings.get_filings_list(comp_cik)
        name = ['income_statement', 'balance_sheet', 'cash_flow']
        financial_statement = filings.get_financials(
            comp_cik,
            submission,
            form,
        )
        financial_statement = {
            name[i]: x for i, x in enumerate(financial_statement)
        }
        return financial_statement

    def get_std_financials(self, which_financial: str,
                           period: str = 'annual') -> pd.DataFrame:
        std_financial = financials.get_std_financials(
            ticker=self.ticker,
            which_financial=which_financial,
            period=period,
        )
        return std_financial
