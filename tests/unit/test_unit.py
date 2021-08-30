import datetime
from financialdatapy import price


def test_parsing_date():
    date = price.Price('AAPL', (2021, 8, 1), (2021, 8, 10))
    assert date.start == 1627743600
    assert date.end == 1628521200
