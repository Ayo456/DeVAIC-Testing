import email.utils
from typing import Optional

def parse_date(ims: str) -> Optional[int]:
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