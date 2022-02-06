from dotenv import load_dotenv
from typing import Optional
import os


class EmptyApiKeyException(Exception):

    def __init__(self, msg: Optional[str] = None, *args, **kwargs) -> None:
        if msg is None:
            msg = ('No API key is provided.'
                   'Check out the documentation for more details.')
        super().__init__(msg, *args, **kwargs)


class Dart:

    def __init__(self, dart_api_key: Optional[str] = None) -> None:
        self.dart_api_key = dart_api_key

    @property
    def dart_api_key(self) -> str:
        return self._dart_api_key

    @dart_api_key.setter
    def dart_api_key(self, dart_api_key: Optional[str] = None) -> None:
        if dart_api_key is None:
            load_dotenv()
            self._dart_api_key = os.environ.get('DART_API_KEY')
            if self._dart_api_key is None:
                raise EmptyApiKeyException()
        else:
            self._dart_api_key = dart_api_key
