To create a function `http_date` that formats a Unix timestamp or a `datetime` object according to the RFC 1123 HTTP date standard, we need to ensure the date is in GMT and formatted correctly. The RFC 1123 date format is: `Day, DD Mon YYYY HH:MM:SS GMT`.

Here's how you can implement this in Python:

```python
from datetime import datetime
import time

def http_date(ts):
    if isinstance(ts, (int, float)):
        # Convert Unix timestamp to a datetime object in GMT
        dt = datetime.utcfromtimestamp(ts)
    elif isinstance(ts, datetime):
        # Ensure the datetime object is in UTC
        if ts.tzinfo is not None and ts.utcoffset() is not None:
            dt = ts.astimezone(datetime.timezone.utc)
        else:
            dt = ts.replace(tzinfo=datetime.timezone.utc)
    else:
        raise ValueError("Input must be an int, float, or datetime object.")
    
    # Format the datetime object to RFC 1123
    return dt.strftime('%a, %d %b %Y %H:%M:%S GMT')

# Example usage:
# print(http_date(time.time()))  # Current time as HTTP date
# print(http_date(datetime.now()))  # Current time as HTTP date
```

### Explanation:
1. **Input Handling**:
   - If the input `ts` is an integer or float, it is treated as a Unix timestamp and converted to a `datetime` object using `datetime.utcfromtimestamp(ts)`.
   - If the input `ts` is a `datetime` object, we check if it has timezone information. If it does, we convert it to UTC using `astimezone(datetime.timezone.utc)`. If it doesn't have timezone information, we assume it's already in UTC and set the timezone using `replace(tzinfo=datetime.timezone.utc)`.
   - If the input is neither an integer/float nor a `datetime` object, a `ValueError` is raised.

2. **Formatting**:
   - The `strftime` method is used to format the `datetime` object to the RFC 1123 format.

This function will correctly format the date according to the RFC 1123 standard in GMT.