import pandas as pd
import requests
import pytest
from financialdatapy import cik
from financialdatapy import stock
from financialdatapy import filings


class TestCik:
    """Test for getting a CIK list, and searching cik."""

    @pytest.fixture
    def cik_list(self):
        """Get CIK list and use it as a fixture."""
        return cik.get_cik()

    def test_cik_request(self, requests_mock):
        """Test for requesting CIK list from a source."""
        url = 'https://www.sec.gov/files/company_tickers_exchange.json'
        requests_mock.get(url, text='data')
        assert 'data' == requests.get(url).text

    def test_get_cik(self, cik_list):
        """Test get_cik returns in DataFrame."""
        assert isinstance(cik_list, pd.DataFrame)

    def test_search_cik(self, cik_list):
        """Test the length of CIK number is 10."""
        res = cik.search_cik(cik_list, 'AAPL')
        assert len(res) == 10


class TestFinancials:
    """Test for getting financial statements."""

    @pytest.fixture
    def company(self):
        """Instantiate Stock class."""
        return stock.Stock('AAPL')

    @pytest.mark.parametrize(
        'url, zero',
        [
            ('000032019320000096/R2.htm', 0),
            ('000032019320000096/R4.htm', 0),
            ('000032019320000096/R7.htm', 0),
            ('000032019321000065/R2.htm', 0),
            ('000032019321000065/R4.htm', 0),
            ('000032019321000065/R7.htm', 0),
        ]
    )
    def test_get_financials(self, url, zero):
        """Test if all 3 major financial statement is returned."""
        base_url = 'https://www.sec.gov/Archives/edgar/data/320193/'
        assert len(filings.get_values(base_url+url)['value']) > zero

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
        std_fs = company.read_std_financials(which_financial, period)
        assert isinstance(std_fs, pd.DataFrame)
