import requests
import json
from bs4 import BeautifulSoup


class ConnectionError(Exception):
    pass


# Request data from sec.gov
class Request():
    def __init__(self, url: str) -> None:
        self.url = url

    def http_request(self) -> requests.models.Response:
        headers = {'User-Agent': 'Mozilla'}
        res = requests.get(self.url, headers=headers)

        if not res.ok:
            raise ConnectionError('Bad response')

        return res

    def get_json(self) -> dict:
        res = self.http_request()
        json_file = json.loads(res.text)

        return json_file

    def get_soup(self) -> BeautifulSoup:
        res = self.http_request()
        soup = BeautifulSoup(res.text, 'html.parser')

        return soup
