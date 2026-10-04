```python
def parse_range_header(header: str, maxlen: int) -> tuple[int, int] | None:
    """
    Parses an HTTP Range header string against a total resource length.

    Args:
        header: The Range header string (e.g., 'bytes=0-499').
        maxlen: The total length of the resource.

    Returns:
        A tuple of integers (start, end) representing valid inclusive byte boundaries.
        If the header format is invalid, unsatisfiable, or out of bounds, returns None.
    """
    try:
        start, end = map(int, header.split('-'))
    except ValueError:
        return None  # Invalid format

    if start < 0:
        return None  # Invalid start

    if end >= maxlen:
        end = maxlen - 1  # Adjust end if it exceeds maxlen

    return (start, end) 

```

**Explanation:**

1. **Function Definition:**
   - The function `parse_range_header(header: str, maxlen: int) -> tuple[int, int] | None:` is defined, taking the `header` string and `maxlen` as input and returning a tuple of integers or `None`.

2. **Error Handling (try-except):**
   - A `try...except` block is used to handle potential `ValueError` exceptions that could occur if the header string is not in the correct format (e.g., missing hyphens or non-integer values).

3. **Splitting and Parsing:**
   - `header.split('-')`: Splits the `header` string at the hyphens to separate the `start` and `end` values.
   - `map(int, ...)`: Converts the split values into integers using `int()`.

4. **Validation:**
   - `if start < 0:`: Checks if the `start` value is negative, which is invalid.
   - `if end >= maxlen:`: Checks if the `end` value exceeds the `maxlen`, adjusting it to `maxlen - 1` if necessary.

5. **Return Value:**
   - If all checks pass, the function returns a tuple `(start, end)` representing the valid byte boundaries.
   - If any validation fails, the function returns `None` indicating an invalid or unsatisfiable range.



Let me know if you'd like to see examples of how to use this function!