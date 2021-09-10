from typing import Optional
import pandas as pd
from financialdatapy import request
from financialdatapy.date import date_to_timestamp


class Price:
    """A Class representing a company's historical stock price data.

    Class Attributes:
        one_day_in_timestamp: Timestamp value equivalent to one day. 
            24hr * 3,600sec/hr = 86,400

    Attributes:
        ticker: Ticker of a company/stock.
        start: Starting date to search. If empty, 1900-01-01 is passed.
        end: Ending date to search. If empty, date of today is passed.

    Methods:
        date_to_timestamp(period: str) -> int:
            Parse the date in string passed by an argument into a timestamp.
        get_price_data() -> dict:
            Get historical stock price data from finance.yahoo.com.
    """
    one_day_in_timestamp = 86_400

    def __init__(self, ticker: str, start: str, end: str) -> None:
        """Initialize ticker, start date and optional end date to search.

        Args:
            ticker: Ticker of a company/stock.
            start: Starting date to search.
            end: Ending date to search. One more day will be added to the
                end date internally for the date range to correctly include
                the end date. Otherwise, the date range will be until the day
                before the end date.
        """
        self.ticker = ticker
        self.start_date_in_timestamp = date_to_timestamp(start)
        self.end_date_in_timestamp = (
            date_to_timestamp(end) + Price.one_day_in_timestamp
        )

    def get_price_data(self) -> pd.DataFrame:
        """Get historical stock price data from finance.yahoo.com.

        Returns:
            Historical stock price data in dataframe.
        """
        url = ('https://query1.finance.yahoo.com/v8/finance/chart/'
               f'{self.ticker}?symbol={self.ticker}'
               f'&period1={self.start_date_in_timestamp}'
               f'&period2={self.end_date_in_timestamp}'
               '&interval=1d&corsDomain=finance.yahoo.com')
        res = request.Request(url)
        data = res.get_json()

        timestamp = data['chart']['result'][0]['timestamp']
        price_data = data['chart']['result'][0]['indicators']['quote'][0]
        columns = ['close', 'open', 'high', 'low', 'volume']

        date_range = [pd.to_datetime(x, unit='s').strftime('%Y-%m-%d')
                      for x in timestamp]
        price_table = pd.DataFrame(
            price_data,
            index=date_range,
            columns=columns,
        )
        price_table = price_table.round(2)
        
        return price_table
