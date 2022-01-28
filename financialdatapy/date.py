"""This module parses and converts objects to date format objects"""
from datetime import datetime
from typing import Optional
import pandas as pd


class IntegerDateInputError(Exception):
    """Raised when integer is passed."""
    pass


def _convert_none_to_date() -> datetime:
    today = pd.Timestamp.today().normalize()

    return today


def validate_date(period: str) -> datetime:
    """Validate the format of date passed as a string.

    :param period: Date in string. If None, date of today is assigned.
    :type period: str
    :raises: :class:`IntegerDateInputError`: If integer type object is passed.
    :return: Date with format YYYY-MM-DD or YY-MM-DD.
    :rtype: datetime.datetime
    """
    if isinstance(period, int):
        raise IntegerDateInputError('Date should be in string.')

    try:
        if period is None:
            date = _convert_none_to_date()
        else:
            date = pd.to_datetime(period, yearfirst=True, format='%Y-%m-%d')

        return date
    except (TypeError, ValueError) as e:
        print(e)


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
