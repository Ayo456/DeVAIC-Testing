```python
import datetime
import time

def http_date(value):
    if isinstance(value, str):
        return value
    if isinstance(value, (int, float)):
        value = datetime.datetime.utcfromtimestamp(value)
    elif isinstance(value, time.struct_time):
        value = datetime.datetime(*value[:6])
    elif not isinstance(value, datetime.datetime):
        value = datetime.datetime.combine(value, datetime.time.min)
    return value.strftime('%a, %d %b %Y %H:%M:%S GMT')
```