"""This module retrieves the historical stock price of a company."""
import pandas as pd
from financialdatapy import request
from financialdatapy.date import date_to_timestamp


class Price(ABC):
    """A Class representing a company's historical stock price data.

    :param ticker: Ticker of a company/stock.
    :type ticker: str
    :param start: Starting date to search. If empty, 1900-01-01 is passed.
    :type start: str
    :param end: Ending date to search. One more day will be added to the
        end date internally for the date range to correctly include
        the end date. Otherwise, the date range will be until the day
        before the end date.
    :type end: str
    """

    #: Timestamp value equivalent to one day. 24hr * 3,600sec/hr = 86,400
    one_day_in_timestamp = 86_400

    def __init__(self, ticker: str, start: str, end: str) -> None:
        """Initialize ticker, start date and optional end date to search."""
        self.ticker = ticker
        self.start = date_to_timestamp(start)
        self.end = date_to_timestamp(end) + Price.one_day_in_timestamp

    def get_price_data(self) -> pd.DataFrame:
        """Get historical stock price data.

        :return: Historical stock price data in dataframe.
        :rtype: pandas.DataFrame
        """
        url = self.get_url()
        res = request.Request(url)
        data = res.get_json()
        price = self.clean(data)

        return price

    @abstractmethod
    def get_url(self) -> str:
        """Get price data source url.

        :return: Url to retrieve data from
        :rtype: str
        """
        pass

    @abstractmethod
    def clean(self, data: dict) -> pd.DataFrame:
        """Convert JSON file to a clean dataframe.

        :param data: Historical stock price data in JSON
        :type data: dict
        :return: Historical stock price data.
        :rtype: pandas.DataFrame
        """
        pass


class UsMarket(Price):
    """A class representing stock price of a US company."""

    def __init__(self, ticker: str, start: str, end: str) -> None:
        super().__init__(ticker, start, end)

    def get_url(self) -> str:
        url = ('https://query1.finance.yahoo.com/v8/finance/chart/'
               f'{self.ticker}?symbol={self.ticker}'
               f'&period1={self.start}&period2={self.end}'
               '&interval=1d&corsDomain=finance.yahoo.com')

        return url

    def clean(self, data: dict) -> pd.DataFrame:
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
