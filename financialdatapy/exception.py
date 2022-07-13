class CountryCodeValidationFailed(Exception):
    """Raised when country code is not in alpha-3 code format."""
    pass


class NotAvailable(Exception):
    """Raised when a response is not available."""
    pass


class EmptyDataFrameError(Exception):
    """Raised when retreived dataframe is empty."""
    pass


class StatusMessageException(Exception):
    """Raised when failed in getting requested data from source."""
    pass


class IntegerDateInputError(Exception):
    """Raised when integer is passed in date parameter."""
    pass


class DartError(Exception):
    """Raised when retrieving data from Dart failed."""
    pass


class EmptyApiKeyException(Exception):
    """Raised when Api key is not provided."""
    pass