from datetime import datetime
import time

def http_date(value):
    if isinstance(value, str):
        return value
    if isinstance(value, (int, float)):
        value = datetime.utcfromtimestamp(value)
    elif isinstance(value, time.struct_time):
        value = datetime(*value[:6])
    elif not isinstance(value, datetime):
        raise ValueError('Unsupported type for conversion to HTTP date')
    return value.strftime('%a, %d %b %Y %H:%M:%S GMT')