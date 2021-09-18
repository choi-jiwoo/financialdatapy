import pandas as pd
import pytest
from financialdatapy import cik
from financialdatapy import filings
from financialdatapy import date
from financialdatapy.date import IntegerDateInputError


@pytest.fixture(scope='class')
def cik_list():
    """Get CIK list and use it as a fixture.

    Used in TestCik inside test_integration.py.
    """
    return cik.get_cik_list()


@pytest.fixture(scope='class')
def price(company):
    """Get historical price data.

    Used in class TestPrice.
    """
    return company.historical('2021-8-3', '2021-8-10')


class TestDate:
    """Test date operations."""

    @pytest.mark.parametrize(
        'start, end',
        [
            ('2021-8-3', '2021-8-10'),
            ('2021-08-03', '2021-08-10'),
            ('21-8-3', '21-8-10'),
            ('21-08-03', '21-08-10'),
        ]
    )
    def test_parsing_date(self, start, end):
        """Test the date correctly converts to timestamp."""
        s_timestamp = date.date_to_timestamp(start)
        e_timestamp = date.date_to_timestamp(end) + 86400

        assert s_timestamp == 1627963200
        assert e_timestamp == 1628654400

    def test_empty_start_date(self):
        """Test default start date returns timestamp of 1900-01-01."""
        s_timestamp = date.date_to_timestamp('1900-01-01')

        assert s_timestamp == -2208974400

    def test_empty_end_date(self):
        """Test default end date returns type int which is a timestamp."""
        e_timestamp = date.date_to_timestamp()
        end = pd.to_datetime(e_timestamp, unit='s').normalize()
        today = pd.Timestamp.today().normalize()

        assert end == today

    def test_year_only_date_input(self):
        """Test YYYY format string as an argument returns YYYY-01-01 format."""
        timestamp = date.date_to_timestamp('2021')
        
        assert timestamp == 1609473600

    def test_integer_input_error(self):
        """Test the function returns error when integer is inputted."""
        with pytest.raises(IntegerDateInputError):
            date.date_to_timestamp(1)


@pytest.mark.usefixtures('cik_list')
class TestCik:
    """Test for getting a CIK list, and searching cik."""

    def test_get_cik(self, cik_list):
        """Test get_cik returns DataFrame."""
        assert isinstance(cik_list, pd.DataFrame)

    def test_search_cik(self, cik_list):
        """Test the returned cik number matches with the company's cik number."""
        res = cik.search_cik(cik_list, 'AAPL')
        assert res == '0000320193'


class TestFilings:
    """Test for getting list of filings a company."""

    def test_filings(self):
        """Test get_filings_list returns DataFrame."""
        res = filings.get_filings_list('0000320193')
        assert isinstance(res, pd.DataFrame)


class TestFinancials:
    """Test for getting financial statements."""

    @pytest.mark.parametrize(
        'form',
        [
            '10-K',
            '10-Q',
        ]
    )
    def test_getting_financials_as_reported(self, company, form):
        """Test all 3 major annual or quarterly financials are returned."""
        ic = company.financials(form, 'income_statement')
        bs = company.financials(form, 'balance_sheet')
        cf = company.financials(form, 'cash_flow')
        assert len(ic) > 0
        assert len(bs) > 0
        assert len(cf) > 0

    @pytest.mark.parametrize(
        'which_financial, period',
        [
            ('income_statement', 'annual'),
            ('balance_sheet', 'annual'),
            ('income_statement', 'annual'),
            ('income_statement', 'quarter'),
            ('balance_sheet', 'quarter'),
            ('income_statement', 'quarter'),
        ]
    )
    def test_get_std_financials(self, company, which_financial, period):
        """Test standard financial statement is in DataFrame."""
        std_fs = company.standard_financials(which_financial, period)
        assert isinstance(std_fs, pd.DataFrame)


class TestPriceData:
    """Tests for getting historical stock price data."""

    def test_getting_price_data(self, price):
        """Test the type of historical stock price data is dictionary."""
        assert isinstance(price, pd.DataFrame)

    def test_price_data(self, price):
        """Test stock price data returns OHLC data.""" 
        quotes = ['close', 'open', 'high', 'low', 'volume']
        
        for i, v in enumerate(price.columns):
            assert v == quotes[i]

    def test_date_and_price_match(self, price):
        """Test the price of a stock on a certain day matches together."""
        assert price['close'][0] == 147.36
