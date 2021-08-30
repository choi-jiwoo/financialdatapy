import pytest
from financialdatapy import cik
from financialdatapy import stock


@pytest.fixture
def cik_list():
    """Get CIK list and use it as a fixture.

    Used in TestCik inside test_integration.py.
    """
    return cik.get_cik()


@pytest.fixture
def company():
    """Instantiate Stock class.

    Used in TestFinancials inside test_integration.py.
    """
    return stock.Stock('AAPL')
