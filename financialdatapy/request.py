"""This module requests data from web."""
import requests
import json
from bs4 import BeautifulSoup


class Request():
    """A class sending and receiving http request.

    :param url: Url of the data source.
    :type url: str
    """

    def __init__(self, url: str) -> None:
        """Initialize Response object."""
        self.url = url
        self.res = self.http_request()

    def http_request(self) -> requests.Response:
        """Sends a GET request to a data source url.

        :raises ConnectionError: If the connection failed.
        :return: A response object from the source.
        :rtype: requests.Response
        """
        headers = {'User-Agent': 'Mozilla'}
        res = requests.get(self.url, headers=headers)

        if res.status_code != 200:
            res.raise_for_status()

        return res

    def get_json(self) -> dict:
        """Convert response object's content to dictionary.

        :return: A JSON format data
        :rtype: dict
        """
        return json.loads(self.res.text)

    def get_soup(self) -> BeautifulSoup:
        """Convert response object's content to BeautifulSoup object.

        :return: A HTML format data
        :rtype: Beautifulsoup
        """
        return BeautifulSoup(self.res.text, 'html.parser')
