from dotenv import load_dotenv
from typing import Optional
import os


class Dart:

    def __init__(self, dart_api_key: Optional[str] = None):
        self.dart_api_key = dart_api_key

    @property
    def dart_api_key(self):
        return self._dart_api_key

    @dart_api_key.setter
    def dart_api_key(self, dart_api_key: Optional[str] = None):
        if dart_api_key is None:
            try:
                load_dotenv()
                self._dart_api_key = os.environ.get('DART_API_KEY')
            except Exception as e:
                raise RuntimeError('Empty API key.') from e
        else:
            self._dart_api_key = dart_api_key
