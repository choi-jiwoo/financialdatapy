import pandas as pd
import requests
import pytest
from financialdatapy import cik


@pytest.fixture
def cik_list():
    """Get CIK list and use it as a fixture."""
    return cik.get_cik()

class TestCik:
    """Test for getting a CIK list, and searching cik."""

    def test_cik_request(self, requests_mock):
        """Test for requesting CIK list from a source."""
        url = 'https://www.sec.gov/files/company_tickers_exchange.json'
        requests_mock.get(url, text='data')
        assert 'data' == requests.get(url).text

    def test_get_cik(self, cik_list):
        """Test get_cik returns in Dataframe."""
        assert isinstance(cik_list, pd.DataFrame)

    def test_search_cik(self, cik_list):
        """Test the length of CIK number is 10."""
        res = cik.search_cik(cik_list, 'AAPL')
        assert len(res) == 10
