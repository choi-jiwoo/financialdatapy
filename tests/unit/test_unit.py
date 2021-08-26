import requests
import pytest


@pytest.mark.parametrize(
    'url',
    [
        ('https://www.sec.gov/files/company_tickers_exchange.json'),
        ('http://data.sec.gov/submissions/CIK0000320193.json'),
        ('https://www.sec.gov/cgi-bin/viewer?action=view&cik=320193&'
         'accession_number=0000320193-20-000096&xbrl_type=v'),
        ('https://www.sec.gov/Archives/edgar/data/0000320193/'
         '000032019320000096/R2.htm'),
        ('https://finviz.com/api/statement.ashx?t=AAPL&s=IA'),
    ]
)
def test_http_request(requests_mock, url):
    """Test for requesting CIK list from a source."""
    requests_mock.get(url, text='data')
    assert 'data' == requests.get(url).text
