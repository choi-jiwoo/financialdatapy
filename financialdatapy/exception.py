from typing import Optional


class CountryCodeValidationFailed(Exception):
    """Raised when country code is not in alpha-3 code format."""
    pass


class NotAvailable(Exception):
    """Raised when a company is not listed in the stock exchange.

    :param msg: Error message, defaults to 'Data is not available.'
    :type msg: str, optional
    """
    def __init__(self, msg: str = 'Data is not available.', *args, **kwargs):
        super().__init__(msg, *args, **kwargs)


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


class EmptyDataFrameError(Exception):
    """Raised when retreived dataframe is empty."""
    def __init__(self, msg: str = 'Data is not available.', *args, **kwargs):
        super().__init__(msg, *args, **kwargs)


class StatusMessageException(Exception):
    """Raised when failed in getting requested data from source.

    :param msg: Error message,
        defaults to 'Failed getting data from dart.fss.or.kr.'
    :type msg: str, optional
    """
    def __init__(self,
                 msg: str = 'Failed getting data from dart.fss.or.kr.',
                 *args, **kwargs) -> None:
        """Initialize StatusMessageException."""
        super().__init__(msg, *args, **kwargs)


class IntegerDateInputError(Exception):
    """Raised when integer is passed in date parameter."""
    pass
