from datetime import date
from datetime import datetime
from dateutil.parser import parse
from financialdatapy import request


class Price():
    def __init__(self, ticker: str, start: str, end: str) -> None:
        self.ticker = ticker
        self.start = self.parse_date(start)
        self.end = self.parse_date(end)

    def parse_date(self, period: str) -> int:
        # include exception handling with a date format
        date = parse(period)
        timestamp = int(datetime.timestamp(date))

        return timestamp

    def get_price_data(self) -> dict:
        url = ('https://query1.finance.yahoo.com/v8/finance/chart/'
               f'{self.ticker}?symbol={self.ticker}&'
               f'period1={self.start}&period2={self.end}&'
               'interval=1d&corsDomain=finance.yahoo.com')
        res = request.Request(url)
        data = res.get_json()

        return data
