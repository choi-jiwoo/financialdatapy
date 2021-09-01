from datetime import datetime
from pytz import timezone
from typing import Optional
from financialdatapy import request


class Price():
    def __init__(self, ticker: str, start: str,
                 end: Optional[str] = None) -> None:
        self.ticker = ticker
        self.start = self.parse_date(start)

        if end is None:
            today = datetime.today().strftime('%Y-%m-%d')
            self.end = self.parse_date(today)
        else:
            # add 86,400s (1 day) to the timestamp
            self.end = self.parse_date(end) + 86400

    def parse_date(self, period: str) -> int:
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
               f'{self.ticker}?symbol={self.ticker}&'
               f'period1={self.start}&period2={self.end}&'
               'interval=1d&corsDomain=finance.yahoo.com')
        res = request.Request(url)
        data = res.get_json()

        return data
