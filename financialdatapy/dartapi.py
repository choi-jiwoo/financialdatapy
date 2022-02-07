"""This module calls api key stored in .env file."""
from dotenv import load_dotenv
from typing import Optional
import os
from financialdatapy.exception import EmptyApiKeyException


class Dart:
    """This class represents api key from opendart.fss.or.kr.

    :param dart_api_key: Api key from opendart.fss.or.kr, defaults to None.
    :type dart_api_key: Optional[str], optional
    """

    def __init__(self, dart_api_key: Optional[str] = None) -> None:
        """Initialize Dart."""
        self.dart_api_key = dart_api_key

    @property
    def dart_api_key(self) -> str:
        """Getter method of property dart_api_key.

        :return: Api key from opendart.fss.or.kr
        :rtype: str
        """
        return self._dart_api_key

    @dart_api_key.setter
    def dart_api_key(self, dart_api_key: Optional[str] = None) -> None:
        """Setter method of property dart_api_key.

        :param dart_api_key: Api key from opendart.fss.or.kr, defaults to None.
        :type dart_api_key: Optional[str], optional
        :raises EmptyApiKeyException: Api key is not submitted.
        """
        if dart_api_key is None:
            load_dotenv()
            self._dart_api_key = os.environ.get('DART_API_KEY')
            if self._dart_api_key is None:
                raise EmptyApiKeyException()
        else:
            self._dart_api_key = dart_api_key
