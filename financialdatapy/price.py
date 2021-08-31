from datetime import datetime
from pytz import timezone
from financialdatapy import request


class Price():
    def __init__(self, ticker: str, start: str, end: str) -> None:
        self.ticker = ticker
        self.start = self.parse_date(start)
        # add 86,400s (1 day) to the end date timestamp
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
