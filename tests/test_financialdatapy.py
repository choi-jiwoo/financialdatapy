from dotenv import load_dotenv
import os
import pandas as pd
import pytest
from financialdatapy import cik
from financialdatapy import date
from financialdatapy import filings
from financialdatapy.date import IntegerDateInputError
from financialdatapy.stock import Stock
from financialdatapy.stocklist import StockList
from financialdatapy.companycode import search_code


@pytest.fixture(scope='class')
def api_key():
    load_dotenv()
    api_key = os.environ.get('DART_API_KEY')
    return api_key


@pytest.fixture(scope='class',
                params=[
                    {'symbol': 'AAPL', 'country': 'USA'},
                    {'symbol': '005930', 'country': 'KOR'},
                ])
def company(request):
    """Fixture of company objects for different stocks.

    :param request: Special object that access each parameters.
    :type request: list
    :return: Instance object of :class:`Stock`:.
    :rtype: :class:`Stock`:
    """
    symbol = request.param['symbol']
    country = request.param['country']
    return Stock(symbol, country)


@pytest.fixture(scope='class')
def cik_list():
    """Get CIK list and use it as a fixture.

    Used in TestCik inside test_integration.py.
    """
    return cik.get_cik_list()


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
    def test_parsing_date_to_timestamp(self, start, end):
        """Test the date correctly converts to timestamp."""
        s_timestamp = date.date_to_timestamp(start)
        e_timestamp = date.date_to_timestamp(end) + 86400

        assert s_timestamp == 1627963200
        assert e_timestamp == 1628654400


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
    """Test getting a CIK list, and searching cik."""

    def test_get_cik(self, cik_list):
        """Test get_cik returns DataFrame."""
        assert isinstance(cik_list, pd.DataFrame)

    def test_search_cik(self, cik_list):
        """Test the returned cik number matches with the company's cik number."""
        res = cik.search_cik(cik_list, 'AAPL')
        assert res == '0000320193'


class TestUsaFilings:
    """Test getting list of filings a company."""

    def test_filings(self):
        """Test get_filings_list returns DataFrame."""
        res = filings.get_filings_list('0000320193')
        assert isinstance(res, pd.DataFrame)


class TestFinancials:
    """Test getting financial statement of company"""

    @pytest.mark.parametrize(
        'period',
        [
            'annual',
            'quarter',
        ]
    )
    def test_getting_financials_as_reported(self, company, period):
        """Test all 3 major annual or quarterly financials are returned."""
        ic = company.financials('income_statement', period)
        bs = company.financials('balance_sheet', period)
        cf = company.financials('cash_flow', period)
        assert len(ic) > 0
        assert len(bs) > 0
        assert len(cf) > 0


class TestStandardFinancials:
    """Test getting standard financial statements."""

    @pytest.mark.parametrize(
        'which_financial, period',
        [
            ('income_statement', 'annual'),
            ('balance_sheet', 'annual'),
            ('cash_flow', 'annual'),
            ('income_statement', 'quarter'),
            ('balance_sheet', 'quarter'),
            ('cash_flow', 'quarter'),
        ]
    )
    def test_get_std_financials(self, company, which_financial, period):
        """Test standard financial statement is in DataFrame."""
        std_fs = company.standard_financials(which_financial, period)
        assert isinstance(std_fs, pd.DataFrame)


class TestPriceData:
    """Tests getting historical stock price data."""

    def test_date_and_price_match(self, company):
        """Test the price of a stock on a certain day matches together."""

        price = {
            'symbol': company.symbol,
            'historical_price': company.historical('2021-8-3', '2021-8-10'),
        }
        first_row_close = price['historical_price']['Close'][0]
        if company.country_code == 'USA':
            close = 147.36
        elif company.country_code == 'KOR':
            close = 80200

        assert first_row_close == close


class TestCompanyCodeInKrx:
    """Test validating company name and its code listed in Korea Exchange."""

    def test_getting_company_code(self):
        """Test if company name and its code match."""
        company_code = search_code('삼성전자')
        assert company_code == '005930'

    def test_corp_code_from_dart_api(self, api_key):
        """Test getting corporate code of a stock in dart.fss.or.kr"""
        corp_list = StockList.get_comp_code_list(api_key)
        symbol = '005930'
        result = corp_list[corp_list['stock_code'] == symbol]
        corp_code = result.get('corp_code').item()
        assert corp_code == '00126380'
