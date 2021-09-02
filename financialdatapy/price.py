from datetime import datetime
from pytz import timezone
from typing import Optional
import pandas as pd
from financialdatapy import request


class IntegerDateInputError(Exception):
    """Throws error when integer type is passed in date parameters."""
    pass


class Price():
    def __init__(self, ticker: str, start: str,
                 end: Optional[str] = None) -> None:
        self.ticker = ticker
        self.start_date_in_timestamp = self.parse_date(start)

        if end is None:
            today = datetime.today().strftime('%Y-%m-%d')
            self.end_date_in_timestamp = self.parse_date(today)
        else:
            one_day_in_timestamp = 86_400
            self.end_date_in_timestamp = (self.parse_date(end)
                                          + one_day_in_timestamp)

    def parse_date(self, period: str) -> int:
        if isinstance(period, int):
            raise IntegerDateInputError('Date should be in string.')

        try:
            date = datetime.strptime(period, '%Y-%m-%d')
        except ValueError:
            date = datetime.strptime(period, '%y-%m-%d')

        edt = timezone('Etc/GMT+4')
        edt_date = edt.localize(date)
        timestamp = int(datetime.timestamp(edt_date))

        return timestamp

    def get_price_data(self) -> dict:
        url = ('https://query1.finance.yahoo.com/v8/finance/chart/'
               f'&{self.ticker}?symbol={self.ticker}'
               f'&period1={self.start_date_in_timestamp}'
               f'&period2={self.end_date_in_timestamp}'
               '&interval=1d&corsDomain=finance.yahoo.com')
        res = request.Request(url)
        data = res.get_json()

        return data
