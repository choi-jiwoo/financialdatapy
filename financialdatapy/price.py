from datetime import date
from datetime import datetime
from dateutil.parser import parse


class Price():
    def __init__(self, ticker: str, start: tuple, end: tuple) -> None:
        self.ticker = ticker
        self.start = self.parse_date(start)
        self.end = self.parse_date(end)

    def parse_date(self, period: tuple) -> int:
        ymd = [str(x) for x in period]
        ymd = '-'.join(ymd)
        date = parse(ymd)
        timestamp = int(datetime.timestamp(date))
        return timestamp
