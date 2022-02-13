"""This module requests data from web."""
from typing import Optional
import requests
from bs4 import BeautifulSoup


class Request:
    """A class sending and receiving http request.

    :param url: Url of the data source.
    :type url: str
    :param method: Which http methods to request, defaults to 'get'.
    :type method: str, optional
    :param headers: Http request headers, defaults to `Request.headers`.
    :type headers: dict, optional
    :param params: URL parameters to attach, defaults to None.
    :type params: dict, optional
    :param data: Data to pass when making POST request, defaults to None.
    :type data: Optional[dict], optional
    """

    #: Default headers to send in request.
    headers = {
        'User-Agent': 'Mozilla',
        'X-Requested-With': 'XMLHttpRequest',
    }

    def __init__(self, url: str, method: str = 'get',
                 headers: dict = headers,
                 params: Optional[dict] = None,
                 data: Optional[dict] = None) -> None:
        """Initialize Request."""
        self.url = url
        self.headers = headers
        self.params = params
        self.data = data
        self.res = self.http_request(method)

    def http_request(self, method: str) -> requests.Response:
        """Sends a GET request to a data source url.

        :param method: Which http methods to request.
        :type method: str
        :raises requests.ConnectionError: HTTP connection failure.
        :return: A response object from the source.
        :rtype: requests.Response
        """

        if method == 'post':
            res = requests.post(
                self.url, data=self.data, headers=self.headers
            )
        else:
            res = requests.get(
                self.url, params=self.params, headers=self.headers
                )

        if res.status_code != 200:
            res.raise_for_status()

        return res

    def get_content(self) -> bytes:
        """Return response object in bytes.

        :return: Response object in bytes.
        :rtype: bytes
        """
        return self.res.content

    def get_text(self) -> str:
        """Return response object in string.

        :return: Response object in string.
        :rtype: str
        """
        return self.res.text

    def get_json(self) -> dict:
        """Convert response object's content to dictionary.

        :return: A JSON format data.
        :rtype: dict
        """
        return self.res.json()

    def get_soup(self) -> BeautifulSoup:
        """Convert response object's content to BeautifulSoup object.

        :return: A HTML format data.
        :rtype: Beautifulsoup
        """
        return BeautifulSoup(self.res.text, 'html.parser')
