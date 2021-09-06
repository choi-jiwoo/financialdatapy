import pytest
from financialdatapy import cik
from financialdatapy import stock


@pytest.fixture(scope='module')
def company():
    """Instantiate Stock class."""
    return stock.Stock('AAPL')
