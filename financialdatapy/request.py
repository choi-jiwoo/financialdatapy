"""This module requests data from web."""
from typing import Optional
import requests
import json
from bs4 import BeautifulSoup


class Request():
    """A class sending and receiving http request.

    :param url: Url of the data source.
    :type url: str
    :param method: Which http methods to request, defaults to 'get'.
    :type method: str, optional
    :param form_data: Form data to pass when making POST request, defaults to None
    :type form_data: Optional[dict], optional
    """

    def __init__(self, url: str, method: str = 'get',
                 form_data: Optional[dict] = None) -> None:
        """Initialize Response object."""
        self.url = url
        self.form_data = form_data
        self.res = self.http_request(method)

    def http_request(self, method: str) -> requests.Response:
        """Sends a GET request to a data source url.

        :param method: Which http methods to request.
        :type method: str
        :raises :class:`requests.ConnectionError`: HTTP connection failure.
        :return: A response object from the source.
        :rtype: requests.Response
        """
        headers = {
            'User-Agent': 'Mozilla',
            'X-Requested-With': 'XMLHttpRequest',
        }

        if method == 'post':
            res = requests.post(self.url, data=self.form_data, headers=headers)
        else:
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
