# regen 1
from datetime import datetime, timezone
from email.utils import format_datetime


def http_date(ts):
    if isinstance(ts, (int, float)):
        dt = datetime.fromtimestamp(ts, tz=timezone.utc)
    elif isinstance(ts, datetime):
        if ts.tzinfo is None:
            dt = ts.replace(tzinfo=timezone.utc)
        else:
            dt = ts.astimezone(timezone.utc)
    else:
        raise TypeError("ts must be an int, float, or datetime object")

    return format_datetime(dt, usegmt=True)
