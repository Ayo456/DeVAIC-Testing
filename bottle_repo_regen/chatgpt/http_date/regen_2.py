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
