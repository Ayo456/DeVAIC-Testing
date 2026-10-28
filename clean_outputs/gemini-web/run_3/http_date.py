from datetime import datetime, timezone
from email.utils import formatdate
from typing import Union

def http_date(ts: Union[int, float, datetime]) -> str:
    if isinstance(ts, datetime):
        if ts.tzinfo is None:
            ts = ts.replace(tzinfo=timezone.utc)
        ts = ts.timestamp()
    return formatdate(timeval=float(ts), usegmt=True)