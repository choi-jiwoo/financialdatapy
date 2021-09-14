from datetime import datetime
from typing import Optional
import pandas as pd


class IntegerDateInputError(Exception):
    """Throws error when integer type is passed in date parameters."""
    pass


def _validate_date_format(period: str) -> datetime:
    """Validate the format of date passed as a string.

    Args:
        period: Date in string 

    Raises:
        IntegerDateInputError: Raised when integer is passed as an argument.

    Returns:
        Datetime object in YYYY-MM-DD or YY-MM-DD format.
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
    """Parse the date in string passed by an argument into a timestamp.

    Args:
        period: Date in string. If empty None is assigned.

    Raises:
        IntegerDateInputError: Raised when integer is passed as an argument.

    Returns:
        The timestamp value equivalent to the date passed.
    """
    date = _validate_date_format(period)
    timestamp = date.timestamp()

    return timestamp

