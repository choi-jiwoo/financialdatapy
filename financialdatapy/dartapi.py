"""This module calls api key stored in .env file."""
from dotenv import load_dotenv
from typing import Optional
import os


class EmptyApiKeyException(Exception):
    """Raised when Api key is not provided.

    :param msg: Error message, defaults to None.
    :type msg: Optional[str], optional
    """

    def __init__(self, msg: Optional[str] = None, *args, **kwargs) -> None:
        """Initialize EmptyApiKeyException."""
        if msg is None:
            msg = ('No API key is provided.'
                   'Check out the documentation for more details.')
        super().__init__(msg, *args, **kwargs)


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
        """Getter of dart_api_key."""
        return self._dart_api_key

    @dart_api_key.setter
    def dart_api_key(self, dart_api_key: Optional[str] = None) -> None:
        """Setter of dart_api_key."""
        if dart_api_key is None:
            load_dotenv()
            self._dart_api_key = os.environ.get('DART_API_KEY')
            if self._dart_api_key is None:
                raise EmptyApiKeyException()
        else:
            self._dart_api_key = dart_api_key
