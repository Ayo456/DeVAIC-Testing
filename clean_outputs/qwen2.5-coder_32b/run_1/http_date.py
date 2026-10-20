from datetime import datetime
import time

def http_date(ts):
    if isinstance(ts, (int, float)):
        ts = datetime.utcfromtimestamp(ts)
    return ts.strftime('%a, %d %b %Y %H:%M:%S GMT')