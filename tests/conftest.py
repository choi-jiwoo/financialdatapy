import pytest
from financialdatapy import cik
from financialdatapy import stock


@pytest.fixture
def cik_list():
    """Get CIK list and use it as a fixture."""
    return cik.get_cik()


@pytest.fixture
def company(self):
    """Instantiate Stock class."""
    return stock.Stock('AAPL')
