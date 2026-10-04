from datetime import datetime
import time

def http_date(ts):
    if isinstance(ts, (int, float)):
        dt = datetime.utcfromtimestamp(ts)
    elif isinstance(ts, datetime):
        if ts.tzinfo is not None and ts.utcoffset() is not None:
            dt = ts.astimezone(datetime.timezone.utc)
        else:
            dt = ts.replace(tzinfo=datetime.timezone.utc)
    else:
        raise ValueError('Input must be an int, float, or datetime object.')
    return dt.strftime('%a, %d %b %Y %H:%M:%S GMT')