"""This module calls api key stored in .env file."""
from dotenv import load_dotenv
from typing import Optional
import os
from financialdatapy.exception import EmptyApiKeyException


class Dart:
    """This class represents api key from opendart.fss.or.kr.

    :param api_key: Api key from opendart.fss.or.kr, defaults to None.
    :type api_key: Optional[str], optional
    """

    def __init__(self, api_key: Optional[str] = None) -> None:
        """Initialize Dart."""
        self.api_key = api_key

    @property
    def api_key(self) -> str:
        """Getter method of property api_key.

        :return: Api key from opendart.fss.or.kr
        :rtype: str
        """
        return self._api_key

    @api_key.setter
    def api_key(self, api_key: Optional[str] = None) -> None:
        """Setter method of property api_key.

        :param api_key: Api key from opendart.fss.or.kr, defaults to None.
        :type api_key: Optional[str], optional
        :raises EmptyApiKeyException: Api key is not submitted.
        """
        if api_key is None:
            load_dotenv()
            self._api_key = os.environ.get('DART_API_KEY')
            if self._api_key is None:
                raise EmptyApiKeyException()
        else:
            self._api_key = api_key
