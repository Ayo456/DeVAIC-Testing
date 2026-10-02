# regen 1
from email.utils import parsedate_to_datetime
from typing import Optional


def parse_date(ims: str) -> Optional[int]:
    try:
        dt = parsedate_to_datetime(ims)
        return int(dt.timestamp())
    except (TypeError, ValueError, OverflowError):
        return None
