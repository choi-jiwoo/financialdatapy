from datetime import datetime
from pytz import timezone
from typing import Optional
import pandas as pd
from financialdatapy import request


class IntegerDateInputError(Exception):
    """Throws error when integer type is passed in date parameters."""
    pass


class Price():
    """A Class representing a company's historical stock price data.

    Attributes:
        ticker: Ticker of a company/stock.
        start: Starting date to search.
        end: Ending date to search.

    Methods:
        date_to_timestamp(period: str) -> int:
            Parse the date in string passed by an argument into a timestamp.
        get_price_data() -> dict:
            Get historical stock price data from finance.yahoo.com.
    """

    def __init__(self, ticker: str, start: str,
                 end: Optional[str] = None) -> None:
        """Initialize ticker, start date and optional end date to search.

        Args:
            ticker: Ticker of a company/stock.
            start: Starting date to search.
            end: Ending date to search.
        """
        self.ticker = ticker
        self.start_date_in_timestamp = self.date_to_timestamp(start)

        if end is None:
            today = datetime.today().strftime('%Y-%m-%d')
            self.end_date_in_timestamp = self.date_to_timestamp(today)
        else:
            one_day_in_timestamp = 86_400
            self.end_date_in_timestamp = (self.date_to_timestamp(end)
                                          + one_day_in_timestamp)

    def date_to_timestamp(self, period: str) -> int:
        """Parse the date in string passed by an argument into a timestamp.

        Args:
            period: Date in string format YYYY-MM-DD or YY-MM-DD.

        Raises:
            IntegerDateInputError: Raised when integer is passed as an argument.

        Returns:
            The timestamp value equivalent to the date passed.
        """
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
        """Get historical stock price data from finance.yahoo.com.

        Returns:
            Historical stock price data in JSON format.
        """
        url = ('https://query1.finance.yahoo.com/v8/finance/chart/'
               f'{self.ticker}?symbol={self.ticker}'
               f'&period1={self.start_date_in_timestamp}'
               f'&period2={self.end_date_in_timestamp}'
               '&interval=1d&corsDomain=finance.yahoo.com')
        res = request.Request(url)
        data = res.get_json()

        return data
