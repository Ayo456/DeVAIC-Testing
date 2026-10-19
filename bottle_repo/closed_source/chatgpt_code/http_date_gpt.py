from datetime import datetime, timezone
from email.utils import formatdate, format_datetime


def http_date(ts):
    if isinstance(ts, datetime):
        if ts.tzinfo is None:
            ts = ts.replace(tzinfo=timezone.utc)
        else:
            ts = ts.astimezone(timezone.utc)

        return format_datetime(ts, usegmt=True)

    return formatdate(ts, usegmt=True)