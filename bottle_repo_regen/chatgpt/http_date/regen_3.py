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
