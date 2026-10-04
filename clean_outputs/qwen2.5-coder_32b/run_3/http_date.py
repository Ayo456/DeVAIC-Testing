from datetime import datetime
import time

def http_date(ts):
    if isinstance(ts, (int, float)):
        dt = datetime.utcfromtimestamp(ts)
    elif isinstance(ts, datetime):
        if ts.tzinfo is not None and ts.utcoffset() is not None:
            dt = ts.astimezone(datetime.utcnow().tzinfo)
        else:
            dt = ts.replace(tzinfo=None)
            dt = dt.replace(hour=dt.hour - dt.utcoffset().seconds // 3600) if dt.utcoffset() else dt
    else:
        raise TypeError('ts must be an int, float, or datetime object')
    return dt.strftime('%a, %d %b %Y %H:%M:%S GMT')
print(http_date(time.time()))
print(http_date(datetime.now()))