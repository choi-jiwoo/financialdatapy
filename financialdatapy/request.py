"""This module requests data from web."""

from bs4 import BeautifulSoup
from dotenv import load_dotenv
import os
import requests
from typing import Optional
from urllib.parse import urlsplit
from user_agent import generate_user_agent
from financialdatapy.exception import EmptySecUserAgentException
from financialdatapy.exception import NotAvailable


def get_sec_user_agent() -> str:
    """Get the declaring User-Agent required by SEC EDGAR.

    SEC rejects requests that do not identify the sender, so each user
    must declare their own contact instead of sharing one baked into the
    package.

    :raises EmptySecUserAgentException: Identity is not provided.
    :return: User-Agent in SEC's 'Name email' format.
    :rtype: str
    """
    load_dotenv()
    user_agent = os.environ.get("SEC_USER_AGENT")

    if user_agent is None:
        raise EmptySecUserAgentException(
            "SEC requires a declaring User-Agent. "
            'Set SEC_USER_AGENT to "App Name your@email.com".'
        )

    return user_agent


def get_user_agent() -> str:
    """Get the User-Agent to send to sources other than SEC.

    Some sources reject the outdated browser versions a randomized
    User-Agent tends to produce, so the user can declare their own
    browser's User-Agent instead.

    :return: User-Agent of the user's browser, or a randomized one when
        the user did not declare theirs.
    :rtype: str
    """
    load_dotenv()
    user_agent = os.environ.get("USER_AGENT")

    if user_agent is None:
        return generate_user_agent()

    return user_agent


class Request:
    """A class sending and receiving http request.

    :param url: Url of the data source.
    :type url: str
    :param method: Which http methods to request, defaults to 'get'.
    :type method: str, optional
    :param headers: Http request headers, defaults to None.
    :type headers: dict, optional
    :param params: URL parameters to attach, defaults to None.
    :type params: dict, optional
    :param data: Data to pass when making POST request, defaults to None.
    :type data: Optional[dict], optional
    """

    #: Available types of response data.
    ResponseType = bytes | str | dict | BeautifulSoup

    def __init__(
        self,
        url: str,
        method: str = "get",
        headers: Optional[dict] = None,
        params: Optional[dict] = None,
        data: Optional[dict] = None,
    ) -> None:
        """Initialize Request."""
        self.url = url
        self.method = method
        self.headers = headers
        self.params = params
        self.data = data

    @property
    def headers(self) -> dict:
        """Getter method of property headers.

        :return: Http request headers.
        :rtype: dict
        """
        return self._headers

    @headers.setter
    def headers(self, headers: dict | None) -> None:
        """Setter method of property headers.

        :param headers: Http request headers.
        :type headers: dict or None
        """
        if headers is None:
            headers = self._default_headers()
        self._headers = headers

    def _default_headers(self) -> dict:
        """Build request headers appropriate for the data source.

        :return: Http request headers.
        :rtype: dict
        """
        host = urlsplit(self.url).hostname or ""

        if host == "sec.gov" or host.endswith(".sec.gov"):
            return {
                "User-Agent": get_sec_user_agent(),
            }

        return {
            "User-Agent": get_user_agent(),
            "X-Requested-With": "XMLHttpRequest",
        }

    @property
    def response(self) -> requests.Response:
        """Sends a HTTP request to a data source url.

        :raises: :py:class:`requests.exceptions.HTTPError` An HTTP error occurred.
        :return: A response object from the source.
        :rtype: requests.Response
        """

        if self.method == "post":
            res = requests.post(self.url, data=self.data, headers=self.headers)
        else:
            res = requests.get(self.url, params=self.params, headers=self.headers)

        if res.status_code != 200:
            res.raise_for_status()

        return res

    def response_data(self, res_type: str) -> ResponseType:
        """Return data depending on the data type.

        :param res_type: Type of response data. 'content', 'text', 'json', or
            'beautifulsoup'.
        :type res_type: str
        :raises NotAvailable: Response data is not available.
        :return: Bytes, text, or json file containing requested data.
        :rtype: ResponseType
        """
        match res_type:
            case "content":
                return self.response.content
            case "text":
                return self.response.text
            case "json":
                return self.response.json()
            case "beautifulsoup":
                return BeautifulSoup(self.response.text, "html.parser")
            case _:
                raise NotAvailable("Response type is not valid.")
