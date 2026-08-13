"""This module parses and converts objects to date format objects"""
import pandas as pd
from financialdatapy.exception import IntegerDateInputError


def _convert_none_to_date(start: bool) -> pd.Timestamp:
    """Returns either current date or date 30 days ago.

    If argument passed in start is True, date 30 days ago will be returned.
    Otherwise, date of today will be returned.

    :param start: Whether argument passed is a starting date or an ending date.
    :type start: bool
    :return: Current date.
    :rtype: pandas.Timestamp
    """
    today = pd.Timestamp.today().normalize()

    if start:
        one_month = pd.Timedelta(days=30)
        one_month_ago = today - one_month
        return one_month_ago
    return today


def validate_date(period: str, start: bool = False) -> pd.Timestamp:
    """Validate the format of date passed as a string.

    :param period: Date in string. If None, date of today is assigned.
    :type period: str
    :param start: Whether argument passed is a starting date or an ending date,
        defaults to False.
    :type start: bool, optional
    :raises IntegerDateInputError: If integer type object is passed.
    :return: Date with format YYYY-MM-DD, YY-MM-DD, or YYYY.
    :rtype: pandas.Timestamp
    """
    if isinstance(period, int):
        raise IntegerDateInputError('Input type of period should be in string.')

    if period is None:
        return _convert_none_to_date(start)

    return pd.to_datetime(period, yearfirst=True)


def date_to_timestamp(period: pd.Timestamp) -> int:
    """Parse date passed in into a timestamp.

    :param period: Date object.
    :type period: pandas.Timestamp
    :return: The timestamp value equivalent to the date passed.
    :rtype: int
    """

    date = period.tz_localize(tz='Etc/GMT+4')
    timestamp = int(date.timestamp())
    return timestamp


def convert_date_format(period: pd.Timestamp, format: str) -> str:
    """Convert date object to desired date format.

    :param period: Date object.
    :type period: pandas.Timestamp
    :param format: Desired date format to convert to.
    :type format: str
    :return: Converted date in string.
    :rtype: str
    """
    new_date = period.strftime(format)
    return new_date
