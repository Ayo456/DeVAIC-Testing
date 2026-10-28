from datetime import datetime
import time

def http_date(value):
    if isinstance(value, str):
        return value
    if isinstance(value, (datetime, time.struct_time)):
        return value.strftime('%a, %d %b %Y %H:%M:%S GMT')
    return datetime.utcfromtimestamp(value).strftime('%a, %d %b %Y %H:%M:%S GMT')