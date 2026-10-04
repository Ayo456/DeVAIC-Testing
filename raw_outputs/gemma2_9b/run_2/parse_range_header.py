```python
def parse_range_header(header: str, maxlen: int) -> tuple[int, int] | None:
    """
    Parses an HTTP Range header string against a total resource length.

    Args:
        header: The HTTP Range header string (e.g., 'bytes=0-499').
        maxlen: The total length of the resource in bytes.

    Returns:
        A tuple of integers (start, end) representing valid inclusive byte boundaries.
        Returns None if the header format is invalid, unsatisfiable, or out of bounds.
    """
    if not header.startswith("bytes="):
        return None  # Invalid format

    try:
        start, end = map(int, header[6:].split("-"))
    except ValueError:
        return None  # Invalid format

    if start < 0 or end >= maxlen or start > end:
        return None  # Unsatisfiable or out of bounds

    return (start, end)

```

**Explanation:**

1. **Format Check:**
   - The function first checks if the `header` string starts with "bytes=". If not, it returns `None` because the format is invalid.

2. **Splitting and Conversion:**
   - It extracts the numerical range from the header using `header[6:].split("-")`.
   - `map(int, ...)` converts the split parts (start and end) into integers.

3. **Validation:**
   - It checks for the following conditions:
     - `start < 0`:  The start index cannot be negative.
     - `end >= maxlen`: The end index cannot exceed the resource length.
     - `start > end`: The start index cannot be greater than the end index.
   - If any of these conditions are true, the function returns `None` because the range is unsatisfiable or out of bounds.

4. **Return Valid Range:**
   - If all checks pass, the function returns a tuple `(start, end)` containing the valid byte boundaries.

**Example Usage:**

```python
header = "bytes=0-499"
maxlen = 1000

start, end = parse_range_header(header, maxlen)

if start is not None:
    print(f"Valid Range: {start} - {end}")
else:
    print("Invalid or Unsatisfiable Range")
```



Let me know if you have any other questions.