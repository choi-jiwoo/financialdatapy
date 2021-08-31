import datetime
from financialdatapy import price


def test_parsing_date():
    """Test the date correctly converts to timestamp."""
    date = price.Price('AAPL', '2021-8-3', '2021-8-10')
    assert date.start == 1627963200
    assert date.end == 1628654400
