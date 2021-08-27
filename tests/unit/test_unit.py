import datetime
from financialdatapy import price


def test_parsing_date():
    date = price.Price('AAPL', (2021, 8, 1), (2021, 8, 10))
    res = date.parse_date()
    assert all(isinstance(x, datetime.date) for x in res.values())
