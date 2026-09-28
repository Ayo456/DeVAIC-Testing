# regen 1
from email.utils import parsedate_to_datetime
from typing import Optional


def parse_date(ims: str) -> Optional[int]:
    try:
        dt = parsedate_to_datetime(ims)
        return int(dt.timestamp())
    except (TypeError, ValueError, OverflowError):
        return None

# regen 2
import email.utils
from typing import Optional


def parse_date(ims: str) -> Optional[int]:
    """Parse an HTTP date header string (RFC 1123, RFC 850, or asctime)

    and return an integer Unix timestamp, or None if parsing fails.
    """
    if not isinstance(ims, str):
        return None

    parsed_tuple = email.utils.parsedate(ims)
    if parsed_tuple is None:
        return None

    try:
        timestamp = email.utils.mktime_tz(email.utils.parsedate_tz(ims))
        return int(timestamp)
    except (TypeError, OverflowError, ValueError):
        return None

# regen 3
from email.utils import parsedate_to_datetime
from datetime import datetime, timezone
import calendar

def parse_date(ims: str):
    if not isinstance(ims, str):
        return None
    

    try:
        dt = parsedate_to_datetime(ims)
        if dt is not None:
            if dt.tzinfo is None:
                dt = dt.replace(tzinfo=timezone.utc)
            return int(dt.timestamp())
    except (TypeError, ValueError):
        pass


    try:
        dt = datetime.strptime(ims.strip(), "%a %b %d %H:%M:%S %Y")
        return calendar.timegm(dt.utctimetuple())
    except (TypeError, ValueError):
        return None