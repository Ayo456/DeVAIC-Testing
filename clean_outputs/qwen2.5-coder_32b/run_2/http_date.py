from datetime import datetime
import time

def http_date(ts):
    if isinstance(ts, (int, float)):
        ts = datetime.utcfromtimestamp(ts)
    elif not isinstance(ts, datetime):
        raise TypeError('ts must be an int, float, or datetime object')
    return ts.strftime('%a, %d %b %Y %H:%M:%S GMT')