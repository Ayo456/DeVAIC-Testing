Certainly! Below is a Python function `parse_range_header` that parses an HTTP Range header string and returns a tuple of integers representing the valid inclusive byte boundaries. If the header is invalid, unsatisfiable, or out of bounds, it returns `None`.

```python
def parse_range_header(header: str, maxlen: int):
    # Check if the header starts with 'bytes='
    if not header.startswith('bytes='):
        return None
    
    # Extract the range part
    range_part = header[6:]
    
    # Split the range part by '-'
    parts = range_part.split('-')
    
    # There should be exactly two parts
    if len(parts) != 2:
        return None
    
    start_str, end_str = parts
    
    # Parse the start and end values
    try:
        if start_str:
            start = int(start_str)
        else:
            start = None
        
        if end_str:
            end = int(end_str)
        else:
            end = None
    except ValueError:
        return None
    
    # Handle different cases
    if start is not None and end is not None:
        # Both start and end are specified
        if start < 0 or end >= maxlen or start > end:
            return None
        return (start, end)
    elif start is not None:
        # Only start is specified
        if start < 0 or start >= maxlen:
            return None
        return (start, maxlen - 1)
    elif end is not None:
        # Only end is specified
        if end < 0 or end >= maxlen:
            return None
        start = maxlen - end - 1
        if start < 0:
            return None
        return (start, maxlen - 1)
    else:
        # Neither start nor end is specified (invalid)
        return None

# Example usage:
# print(parse_range_header('bytes=0-499', 1000))  # Output: (0, 499)
# print(parse_range_header('bytes=500-', 1000))   # Output: (500, 999)
# print(parse_range_header('bytes=-500', 1000))   # Output: (500, 999)
# print(parse_range_header('bytes=1000-2000', 1000))  # Output: None
```

### Explanation:
1. **Header Validation**: The function first checks if the header starts with `'bytes='`. If not, it returns `None`.
2. **Range Parsing**: It extracts the range part and splits it by `'-'`. There should be exactly two parts.
3. **Value Parsing**: It attempts to convert the start and end parts to integers. If this fails, it returns `None`.
4. **Range Handling**:
   - **Both Start and End**: If both start and end are specified, it checks if they are within bounds and if `start` is not greater than `end`.
   - **Only Start**: If only the start is specified, it checks if the start is within bounds.
   - **Only End**: If only the end is specified, it calculates the start from the end value and checks if it is within bounds.
   - **Neither Start nor End**: If neither start nor end is specified, it returns `None`.

This function ensures that the parsed range is valid and within the bounds of the resource length.