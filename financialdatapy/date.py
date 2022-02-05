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
        raise IntegerDateInputError('Input type of period should be in string.')

    try:
        if period is None:
            date = _convert_none_to_date()
        else:
            date = pd.to_datetime(period, yearfirst=True, format='%Y-%m-%d')

        return date
    except (TypeError, ValueError) as e:
        raise RuntimeError('Bad input of \'period\'.') from e
def string_to_date(period: str or datetime, date_format: str) -> pd.Timestamp:
    date = pd.to_datetime(period, yearfirst=True, format=date_format)

    return date

def date_to_timestamp(period: datetime) -> int:
    """Parse date passed in into a timestamp.

    :param period: `datetime.datetime` object.
    :type period: `datetime.datetime`
    :return: The timestamp value equivalent to the date passed.
    :rtype: int
    """

    date = period.tz_localize(tz='Etc/GMT+4')
    timestamp = int(date.timestamp())

    return timestamp


def convert_date_format(period: datetime, format: str) -> str:
    new_date = period.strftime(format)

    return new_date
