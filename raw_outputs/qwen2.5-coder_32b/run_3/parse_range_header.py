Certainly! Below is a Python function `parse_range_header` that parses an HTTP Range header string against a total resource length `maxlen`. It returns a tuple of integers `(start, end)` representing valid inclusive byte boundaries. If the header format is invalid, unsatisfiable, or out of bounds, it returns `None`.

```python
def parse_range_header(header: str, maxlen: int) -> tuple:
    # Check if the header starts with 'bytes='
    if not header.startswith('bytes='):
        return None
    
    # Remove 'bytes=' prefix
    range_spec = header[6:]
    
    # Split the range specification by '-'
    parts = range_spec.split('-')
    
    # There should be exactly two parts
    if len(parts) != 2:
        return None
    
    start_str, end_str = parts
    
    # Handle the case where the range is open-ended
    if start_str == '' and end_str == '':
        return None
    
    # Parse start and end values
    try:
        if start_str == '':
            start = maxlen - int(end_str)
            end = maxlen - 1
        elif end_str == '':
            start = int(start_str)
            end = maxlen - 1
        else:
            start = int(start_str)
            end = int(end_str)
    except ValueError:
        return None
    
    # Validate the range
    if start < 0 or end >= maxlen or start > end:
        return None
    
    return (start, end)

# Example usage:
print(parse_range_header('bytes=0-499', 1000))  # Output: (0, 499)
print(parse_range_header('bytes=500-', 1000))   # Output: (500, 999)
print(parse_range_header('bytes=-500', 1000))   # Output: (500, 999)
print(parse_range_header('bytes=1000-2000', 1000))  # Output: None
print(parse_range_header('bytes=-1000', 1000))  # Output: (0, 999)
print(parse_range_header('bytes=1000-999', 1000))  # Output: None
print(parse_range_header('bytes=abc-499', 1000))  # Output: None
```

### Explanation:
1. **Header Validation**: The function first checks if the header starts with `bytes=`. If not, it returns `None`.
2. **Range Specification Parsing**: It removes the `bytes=` prefix and splits the remaining string by `-` to get the start and end values.
3. **Handling Open-Ended Ranges**: It handles cases where either the start or end value is missing.
4. **Parsing and Validating Start and End Values**: It attempts to parse the start and end values as integers. If parsing fails, it returns `None`. It also validates that the start and end values are within the valid range and that `start` is not greater than `end`.
5. **Return Valid Range**: If all checks pass, it returns the valid `(start, end)` tuple. Otherwise, it returns `None`.

This function should cover the typical cases for HTTP Range headers as specified in the HTTP/1.1 standard.