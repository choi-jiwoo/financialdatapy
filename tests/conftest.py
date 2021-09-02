import pytest
from financialdatapy import cik
from financialdatapy import stock


@pytest.fixture
def company():
    """Instantiate Stock class.

    Used in TestFinancials inside test_integration.py.
    """
    return stock.Stock('AAPL')
