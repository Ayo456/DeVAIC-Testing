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
