```python
def _parse_qsl(qs: str) -> list[tuple[str, str]]:
    """Parses a URL query string qs into a list of (name, value) key-value tuples.

    Args:
        qs: The URL query string to parse.

    Returns:
        A list of (name, value) tuples representing the key-value pairs in the query string.
    """
    items = []
    for item in qs.split("&"):
        if item:
            parts = item.split("=", 1)
            name = parts[0].replace("+", " ").decode("ascii")
            value = parts[1] if len(parts) > 1 else None
            value = value.replace("+", " ").decode("ascii") if value else None
            items.append((name, value))
    return items
```

**Explanation:**

1. **Initialization:**
   - `items = []`: Creates an empty list to store the parsed key-value tuples.

2. **Iterating through Query Parameters:**
   - `for item in qs.split("&"):`: Splits the query string `qs` by the `&` delimiter, separating individual parameters.
   - `if item:`: Skips empty items resulting from consecutive `&` characters.

3. **Parsing Each Parameter:**
   - `parts = item.split("=", 1)`: Splits each parameter by the `=` delimiter, limiting the split to at most one occurrence. This handles cases where a parameter has no value.
   - `name = parts[0].replace("+", " ").decode("ascii")`: Extracts the parameter name from the first part, replaces `+` with spaces, and decodes it using ASCII encoding.
   - `value = parts[1] if len(parts) > 1 else None`: Extracts the parameter value if it exists (length of `parts` is greater than 1), otherwise sets it to `None`.
   - `value = value.replace("+", " ").decode("ascii") if value else None`: Decodes the value (if it exists) by replacing `+` with spaces and using ASCII encoding.

4. **Appending to Result:**
   - `items.append((name, value))`: Creates a tuple `(name, value)` and appends it to the `items` list.

5. **Returning the Result:**
   - `return items`: Returns the list of parsed key-value tuples.



Let me know if you have any other questions!