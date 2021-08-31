import pandas as pd
import pytest
from financialdatapy import cik
from financialdatapy import filings
from financialdatapy import price


class TestCik:
    """Test for getting a CIK list, and searching cik."""

    def test_get_cik(self, cik_list):
        """Test get_cik returns DataFrame."""
        assert isinstance(cik_list, pd.DataFrame)

    def test_search_cik(self, cik_list):
        """Test the length of CIK number is 10."""
        res = cik.search_cik(cik_list, 'AAPL')
        assert len(res) == 10


class TestFilings:
    """Test for getting list of filings a company."""

    def test_filings(self):
        """Test get_filings_list returns DataFrame."""
        res = filings.get_filings_list('0000320193')
        assert isinstance(res, pd.DataFrame)


class TestFinancials:
    """Test for getting financial statements."""

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
    def test_getting_each_financials(self, url, zero):
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
        std_fs = company.standard_financials(which_financial, period)
        assert isinstance(std_fs, pd.DataFrame)


class TestPriceData:
    """Tests for getting historical stock price data."""

    def test_getting_price_data(self, company):
        """Test the type of historical stock price data is dictionary."""
        price = company.historical('2021-8-3', '2021-8-10')
        assert isinstance(price, dict)
