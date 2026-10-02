# regen 2
from datetime import datetime, timezone
from email.utils import format_datetime
from typing import Union


def http_date(ts: Union[int, float, datetime]) -> str:
    if isinstance(ts, (int, float)):
        dt = datetime.fromtimestamp(ts, tz=timezone.utc)
    elif isinstance(ts, datetime):
        if dt_is_naive := (ts.tzinfo is None or ts.tzinfo.utcoffset(ts) is None):
            dt = ts.replace(tzinfo=timezone.utc)
        else:
            dt = ts.astimezone(timezone.utc)
    else:
        raise TypeError("ts must be an int, float, or datetime object")

    return format_datetime(dt, usegmt=True)
