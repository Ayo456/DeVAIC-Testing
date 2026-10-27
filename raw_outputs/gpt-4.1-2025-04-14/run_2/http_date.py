```python
import datetime
import time

def http_date(value):
    if isinstance(value, str):
        return value
    if isinstance(value, datetime.datetime):
        dt = value
    elif isinstance(value, datetime.date):
        dt = datetime.datetime(value.year, value.month, value.day)
    elif isinstance(value, (int, float)):
        dt = datetime.datetime.utcfromtimestamp(value)
    elif isinstance(value, time.struct_time):
        dt = datetime.datetime(*value[:6])
    else:
        raise TypeError("Unsupported type for http_date")
    weekday = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"][dt.weekday()]
    month = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"][dt.month - 1]
    return "%s, %02d %s %04d %02d:%02d:%02d GMT" % (
        weekday, dt.day, month, dt.year, dt.hour, dt.minute, dt.second
    )
```