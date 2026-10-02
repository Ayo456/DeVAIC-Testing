# regen 3
from datetime import datetime, timezone
from email.utils import formatdate
from typing import Union


def http_date(ts: Union[int, float, datetime]) -> str:
    """Return an RFC 1123 / HTTP-formatted date string in GMT."""
    if isinstance(ts, datetime):
        if ts.tzinfo is None:
            ts = ts.replace(tzinfo=timezone.utc)
        ts = ts.timestamp()

    return formatdate(timeval=float(ts), usegmt=True)
