# regen 1
from datetime import datetime, timezone
from email.utils import format_datetime

def http_date(ts):
    if isinstance(ts, datetime):
        dt = ts
        if dt.tzinfo is None:
            dt = dt.replace(tzinfo=timezone.utc)
        else:
            dt = dt.astimezone(timezone.utc)
    elif isinstance(ts, (int, float)):
        dt = datetime.fromtimestamp(ts, timezone.utc)
    else:
        raise TypeError("ts must be an int, float, or datetime object")

    return format_datetime(dt, usegmt=True)
