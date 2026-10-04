```python
import datetime

def http_date(ts):
  """
  Formats a Unix timestamp to an RFC 1123 HTTP date string in GMT.

  Args:
    ts: An integer or float representing a Unix timestamp, or a datetime object.

  Returns:
    A formatted date string conforming to RFC 1123 HTTP date standard in GMT.
  """
  if isinstance(ts, datetime.datetime):
    dt = ts
  else:
    dt = datetime.datetime.fromtimestamp(ts)
  
  return dt.strftime("%a, %d %b %Y %H:%M:%S GMT")


# Example usage
timestamp = 1678886400
date_string = http_date(timestamp)
print(date_string)  # Output: Tue, 14 Mar 2023 00:00:00 GMT
```

**Explanation:**

1. **Import `datetime`:** This line imports the necessary library for working with dates and times.
2. **Define `http_date(ts)` Function:** This function takes a timestamp (`ts`) as input, which can be either an integer, a float, or a `datetime` object.
3. **Handle Different Input Types:** The code checks the type of `ts`. If it's already a `datetime` object, it assigns it directly to `dt`. Otherwise, it converts the timestamp to a `datetime` object using `datetime.datetime.fromtimestamp(ts)`.
4. **Format the Date String:** The `strftime()` method is used to format the `dt` object according to the RFC 1123 standard:
   - `%a`: Abbreviated weekday name (e.g., "Tue")
   - `%d`: Day of the month (e.g., "14")
   - `%b`: Abbreviated month name (e.g., "Mar")
   - `%Y`: Year with century (e.g., "2023")
   - `%H`: Hour (24-hour clock) (e.g., "00")
   - `%M`: Minute (e.g., "00")
   - `%S`: Second (e.g., "00")
   - `GMT`:  Specifies the time zone as Greenwich Mean Time.

5. **Return the Formatted String:** The function returns the formatted date string.

**Example Usage:**

The example code demonstrates how to use the `http_date()` function with a Unix timestamp. It prints the resulting RFC 1123 formatted date string.