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

# regen 2
from datetime import datetime, timezone
from email.utils import format_datetime

def http_date(ts):
    if isinstance(ts, datetime):
        dt = ts
        if dt.tzinfo is None:
            dt = dt.replace(tzinfo=timezone.utc)
        else:
            dt = dt.astimezone(timezone.utc)
    else:
        dt = datetime.fromtimestamp(ts, timezone.utc)

    return format_datetime(dt, usegmt=True)

# regen 3
from datetime import datetime, timezone

def http_date(ts) -> str:
    if isinstance(ts, datetime):
        if ts.tzinfo is None:
            dt = ts.replace(tzinfo=timezone.utc)
        else:
            dt = ts.astimezone(timezone.utc)
    else:
        dt = datetime.fromtimestamp(ts, timezone.utc)

    return dt.strftime("%a, %d %b %Y %H:%M:%S GMT")