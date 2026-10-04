from datetime import datetime
import time

def http_date(ts):
    if isinstance(ts, (int, float)):
        dt = datetime.utcfromtimestamp(ts)
    elif isinstance(ts, datetime):
        if ts.tzinfo is not None:
            dt = ts.astimezone(datetime.utcnow().tzinfo)
        else:
            dt = ts.replace(tzinfo=None)
            dt = dt.astimezone(datetime.utcnow().tzinfo)
    else:
        raise ValueError('The input must be an integer, float, or datetime object.')
    return dt.strftime('%a, %d %b %Y %H:%M:%S GMT')
print(http_date(time.time()))
print(http_date(datetime.now()))