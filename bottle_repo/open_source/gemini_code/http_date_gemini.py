from datetime import datetime, timezone
import email.utils
from typing import Union

def http_date(ts: Union[int, float, datetime]) -> str:
    if isinstance(ts, datetime):
        if ts.tzinfo is None:
            ts = ts.replace(tzinfo=timezone.utc)
        else:
            ts = ts.astimezone(timezone.utc)
        timestamp = ts.timestamp()
    else:
        timestamp = float(ts)

    return email.utils.formatdate(timeval=timestamp, usegmt=True)