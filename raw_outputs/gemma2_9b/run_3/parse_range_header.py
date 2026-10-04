```python
def parse_range_header(header: str, maxlen: int) -> tuple[int, int] | None:
    """
    Parses an HTTP Range header string against a total resource length maxlen.

    Args:
        header: The Range header string (e.g., 'bytes=0-499').
        maxlen: The total length of the resource.

    Returns:
        A tuple of integers (start, end) representing valid inclusive byte boundaries.
        Returns None if the header format is invalid, unsatisfiable, or out of bounds.
    """

    try:
        # Extract the range from the header
        _, start_end = header.split("=")
        start, end = map(int, start_end.split("-"))
    except ValueError:
        return None  # Invalid format

    # Handle edge cases:
    if start < 0:
        return None  # Invalid start position
    if end >= maxlen:
        return None  # Range exceeds resource length

    if end < start:
        return None  # Invalid range (end before start)

    return (start, end)
```

**Explanation:**

1. **Function Signature:**
   - `parse_range_header(header: str, maxlen: int) -> tuple[int, int] | None:`
     - Takes a `header` string and `maxlen` as input.
     - Returns a tuple of integers `(start, end)` or `None`.

2. **Error Handling (try-except):**
   - The code is wrapped in a `try-except` block to handle `ValueError` exceptions that might occur if the header format is incorrect.

3. **Header Parsing:**
   - `_, start_end = header.split("=") `: Splits the header at the `=` sign, keeping the range part.
   - `start, end = map(int, start_end.split("-"))`: Splits the range string at the `-` sign and converts the parts to integers.

4. **Range Validation:**
   - `if start < 0:`: Checks if the start position is negative (invalid).
   - `if end >= maxlen:`: Checks if the end position exceeds the resource length.
   - `if end < start:`: Checks if the end position is before the start position (invalid range).

5. **Return Value:**
   - If all checks pass, returns the `(start, end)` tuple.
   - If any validation fails, returns `None` to indicate an invalid or unsatisfiable range.



Let me know if you'd like to see examples of how to use this function!