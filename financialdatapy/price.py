"""This module retrieves the historical stock price of a company."""
from abc import ABC, abstractmethod
import pandas as pd
from financialdatapy.date import date_to_timestamp
from financialdatapy.date import convert_date_format
from financialdatapy.request import Request
from financialdatapy import search


class Price(ABC):
    """A Class representing a company's historical stock price data.

    :param symbol: Symbol of a company/stock.
    :type symbol: str
    :param start: Starting date to search.
    :type start: pandas.Timestamp
    :param end: Ending date to search.
    :type end: pandas.Timestamp
    """

    def __init__(self, symbol: str,
                 start: pd.Timestamp,
                 end: pd.Timestamp) -> None:
        """Initialize Price"""
        self.symbol = symbol
        self.start = start
        self.end = end

    @abstractmethod
    def _get_raw_price_data(self):
        pass

    @abstractmethod
    def get_price_data(self):
        pass


class UsMarket(Price):
    """A class representing stock price of a US company."""

    def _get_raw_price_data(self) -> dict:
        """Get historical stock price data from source in a raw form.

        :return: Historical stock price data retrieved in JSON file.
        :rtype: dict
        """
        one_day_in_timestamp = 86_400
        start_date_timestamp = date_to_timestamp(self.start)
        end_date_timestamp = (date_to_timestamp(self.end) +
                              one_day_in_timestamp)
        url = ('https://query1.finance.yahoo.com/v8/finance/chart/'
               f'{self.symbol}?symbol={self.symbol}'
               f'&period1={start_date_timestamp}&period2={end_date_timestamp}'
               '&interval=1d&corsDomain=finance.yahoo.com')
        res = Request(url)
        data = res.get_json()

        return data

    def get_price_data(self) -> pd.DataFrame:
        """Get historical stock price data.

        :param data: Historical stock price data in JSON
        :type data: dict
        :return: Historical stock price data.
        :rtype: pandas.DataFrame
        """
        data = self._get_raw_price_data()
        timestamp = data['chart']['result'][0]['timestamp']
        price_data = data['chart']['result'][0]['indicators']['quote'][0]
        columns = ['Date', 'close', 'open', 'high', 'low', 'volume']

        date_range = [pd.to_datetime(x, unit='s').strftime('%Y-%m-%d')
                      for x
                      in timestamp]
        price_data['Date'] = date_range

        price_table = pd.DataFrame(
            price_data,
            columns=columns,
        )
        price_table = price_table.round(2)
        table_col = price_table.columns.tolist()
        price_table.columns = [x.capitalize() for x in table_col]

        return price_table


class KorMarket(Price):
    """A class representing stock price of a South Korea company."""

    def _get_raw_price_data(self) -> pd.DataFrame:
        """Get historical stock price data from source in a raw form.

        :return: Historical stock price data retrieved in JSON file.
        :rtype: dict
        """

        date_format = '%m/%d/%Y'
        st_date = convert_date_format(self.start, date_format)
        end_date = convert_date_format(self.end, date_format)

        url = 'https://www.investing.com/instruments/HistoricalDataAjax'
        company_search_result = search.Company(self.symbol)
        curr_id = company_search_result.search_pair_id()
        data = {
            'curr_id': curr_id,
            'st_date': st_date,
            'end_date': end_date,
            'interval_sec': 'Daily',
            'action': 'historical_data',
        }
        res = Request(url, method='post', data=data)
        data = res.get_text()
        tables = pd.read_html(data)
        historical_price = tables[0]

        return historical_price

    def get_price_data(self) -> pd.DataFrame:
        """Get historical stock price data.

        :return: Historical stock price data.
        :rtype: pandas.DataFrame
        """
        data = self._get_raw_price_data()
        data = data.replace(r'-$', float('NaN'), regex=True)

        data.dropna(inplace=True)
        data.reset_index(drop=True, inplace=True)
        data.drop('Change %', axis=1, inplace=True)

        data.rename(columns={'Price': 'Close', 'Vol.': 'Volume'}, inplace=True)

        data['Volume'] = data['Volume'].apply(
            lambda x: float(x[:-1]) * 1000000
            if x[-1] == 'M'
            else float(x[:-1]) * 1000
        )
        data['Volume'] = data['Volume'].astype('int')
        data['Date'] = pd.to_datetime(data['Date'])

        return data
