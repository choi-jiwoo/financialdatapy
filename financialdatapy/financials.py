"""This module states abstract class for financial statements."""
from abc import ABC, abstractmethod
from typing import Optional
import pandas as pd


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
    def get_financials(self) -> pd.DataFrame:
        pass

    @abstractmethod
    def get_standard_financials(self) -> pd.DataFrame:
        pass
