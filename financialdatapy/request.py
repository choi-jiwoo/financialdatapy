import requests
import json
from bs4 import BeautifulSoup


class ConnectionError(Exception):
    pass


class Request():
    def __init__(self, url: str) -> None:
        self.url = url
        self.res = self.http_request()

    def http_request(self) -> requests.models.Response:
        headers = {'User-Agent': 'Mozilla'}
        res = requests.get(self.url, headers=headers)

        if not res.ok:
            raise ConnectionError(f'Status code<{res.status_code}>')

        return res

    def get_json(self) -> dict:
        return json.loads(self.res.text)

    def get_soup(self) -> BeautifulSoup:
        return BeautifulSoup(self.res.text, 'html.parser')
