import requests


def test_cik_request(requests_mock):
    """Test for requesting CIK list from a source."""
    url = 'https://www.sec.gov/files/company_tickers_exchange.json'
    requests_mock.get(url, text='data')
    assert 'data' == requests.get(url).text
