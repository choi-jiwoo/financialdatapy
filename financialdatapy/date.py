"""This module parses and converts objects to date format objects"""
from datetime import datetime
from typing import Optional
import pandas as pd


class IntegerDateInputError(Exception):
    """Raised when integer is passed."""
    pass


def _validate_date_format(period: str) -> datetime:
    """Validate the format of date passed as a string.

    :param period: Date in string. If None, date of today is assigned.
    :type period: str
    :raises: :class:`IntegerDateInputError`: If integer type object is passed.
    :return: Date with format YYYY-MM-DD or YY-MM-DD.
    :rtype: datetime.datetime
    """
    if isinstance(period, int):
        raise IntegerDateInputError('Date should be in string.')

    if period is None:
        date = pd.Timestamp.today().normalize()
    else:
        date = pd.to_datetime(period, yearfirst=True)

    date = date.tz_localize(tz='Etc/GMT+4')

    return date


def date_to_timestamp(period: Optional[str] = None) -> int:
    """Parse date passed by an argument as string into a timestamp.

    :param period: Date in string. If empty, None is assigned.
    :type period: str, optional
    :return: The timestamp value equivalent to the date passed.
    :rtype: int
    """
    date = _validate_date_format(period)
    timestamp = int(date.timestamp())

    return timestamp
