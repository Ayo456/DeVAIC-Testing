To create a function `http_date` that formats a Unix timestamp or a `datetime` object into an RFC 1123 compliant HTTP date string in GMT, we can use Python's `datetime` module. The RFC 1123 format is specified as `Wdy, DD Mon YYYY HH:MM:SS GMT`.

Here's how you can implement this function:

```python
from datetime import datetime
import time

def http_date(ts):
    if isinstance(ts, (int, float)):
        # Convert the Unix timestamp to a datetime object in GMT
        dt = datetime.utcfromtimestamp(ts)
    elif isinstance(ts, datetime):
        # Ensure the datetime object is in UTC
        if ts.tzinfo is not None and ts.utcoffset() is not None:
            dt = ts.astimezone(datetime.utcnow().tzinfo)
        else:
            dt = ts.replace(tzinfo=None)
            dt = dt.replace(hour=dt.hour - dt.utcoffset().seconds // 3600) if dt.utcoffset() else dt
    else:
        raise TypeError("ts must be an int, float, or datetime object")
    
    # Format the datetime object as an RFC 1123 date string
    return dt.strftime('%a, %d %b %Y %H:%M:%S GMT')

# Example usage:
print(http_date(time.time()))  # Current time as an HTTP date string
print(http_date(datetime.now()))  # Current datetime as an HTTP date string
```

### Explanation:
1. **Input Handling**:
   - If `ts` is an integer or float, it is assumed to be a Unix timestamp. We convert it to a `datetime` object using `datetime.utcfromtimestamp(ts)`, which automatically sets the timezone to UTC.
   - If `ts` is a `datetime` object, we check if it already has timezone information. If it does, we convert it to UTC using `astimezone(datetime.utcnow().tzinfo)`. If it doesn't have timezone information, we assume it is already in UTC and proceed.
   - If `ts` is neither an integer/float nor a `datetime` object, we raise a `TypeError`.

2. **Date Formatting**:
   - We use `strftime` with the format string `'%a, %d %b %Y %H:%M:%S GMT'` to format the `datetime` object into the required RFC 1123 format.

This function should work correctly for both Unix timestamps and `datetime` objects, ensuring the output is always in GMT as per the RFC 1123 standard.