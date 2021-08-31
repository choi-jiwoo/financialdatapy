import pytest
from financialdatapy import price


@pytest.mark.parametrize(
    'start, end',
    [
        ('2021-8-3', '2021-8-10'),
        ('2021-08-03', '2021-08-10'),
        ('21-8-3', '21-8-10'),
        ('21-08-03', '21-08-10'),
    ]
)
def test_parsing_date(start, end):
    """Test the date correctly converts to timestamp."""
    date = price.Price('AAPL', start, end)
    assert date.start == 1627963200
    assert date.end == 1628654400
