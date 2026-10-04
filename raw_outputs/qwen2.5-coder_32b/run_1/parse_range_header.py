Certainly! Below is a Python function `parse_range_header` that parses an HTTP `Range` header string and returns a tuple of integers representing the valid inclusive byte boundaries. If the header is invalid, unsatisfiable, or out of bounds, it returns `None`.

```python
def parse_range_header(header: str, maxlen: int):
    # Check if the header starts with 'bytes='
    if not header.startswith('bytes='):
        return None
    
    # Remove 'bytes=' prefix
    range_spec = header[6:]
    
    # Split the range specification by '-'
    parts = range_spec.split('-')
    
    # Ensure we have exactly two parts
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
    
    # Handle the case where both start and end are None
    if start is None and end is None:
        return None
    
    # Handle the case where only end is specified (suffix range)
    if start is None and end is not None:
        if end > maxlen:
            return None
        start = maxlen - end
        end = maxlen - 1
    
    # Handle the case where only start is specified (prefix range)
    if start is not None and end is None:
        if start >= maxlen:
            return None
        end = maxlen - 1
    
    # Handle the case where both start and end are specified
    if start is not None and end is not None:
        if start >= maxlen or end >= maxlen or start > end:
            return None
    
    return (start, end)

# Example usage:
# print(parse_range_header('bytes=0-499', 1000))  # Output: (0, 499)
# print(parse_range_header('bytes=-500', 1000))   # Output: (500, 999)
# print(parse_range_header('bytes=500-', 1000))   # Output: (500, 999)
# print(parse_range_header('bytes=1000-', 1000))  # Output: None
# print(parse_range_header('bytes=500-499', 1000)) # Output: None
```

### Explanation:
1. **Header Validation**: The function first checks if the header starts with `bytes=`.
2. **Range Specification Parsing**: It then splits the range specification by `-` and ensures there are exactly two parts.
3. **Start and End Parsing**: The function attempts to parse the start and end values as integers. If parsing fails, it returns `None`.
4. **Suffix Range Handling**: If only the end is specified (e.g., `bytes=-500`), it calculates the start based on the total length.
5. **Prefix Range Handling**: If only the start is specified (e.g., `bytes=500-`), it sets the end to the maximum length minus one.
6. **Bounds Checking**: The function checks if the start and end values are within the valid range and ensures that the start does not exceed the end.
7. **Return**: If all checks pass, it returns a tuple of the start and end values; otherwise, it returns `None`.