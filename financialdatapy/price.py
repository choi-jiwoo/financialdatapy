from datetime import date
from datetime import datetime
from dateutil.parser import parse


class Price():
    def __init__(self, ticker: str, start: tuple, end: tuple) -> None:
        self.ticker = ticker
        self.start = start
        self.end = end

    def parse_date(self) -> None:
        start = date(*self.start)
        end = date(*self.end)
        date_range = {'start': start, 'end': end}
        return date_range
