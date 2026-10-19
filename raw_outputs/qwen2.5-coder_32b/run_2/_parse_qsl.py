Certainly! Below is a Python function named `_parse_qsl` that parses a URL query string `qs` into a list of `(name, value)` key-value tuples. The function handles percent-encoded characters, replaces `+` characters with spaces, and manages parameterless or blank segments gracefully.

```python
import urllib.parse

def _parse_qsl(qs: str) -> list:
    # Split the query string by '&' to get individual key-value pairs
    pairs = qs.split('&')
    
    # Initialize an empty list to store the parsed key-value tuples
    result = []
    
    for pair in pairs:
        # Skip empty segments
        if not pair:
            continue
        
        # Split each pair by '=' to separate the key and value
        if '=' in pair:
            key, value = pair.split('=', 1)
        else:
            # If there's no '=', treat the whole segment as a key with an empty value
            key = pair
            value = ''
        
        # Replace '+' with spaces in both key and value
        key = key.replace('+', ' ')
        value = value.replace('+', ' ')
        
        # Decode percent-encoded characters in both key and value
        key = urllib.parse.unquote(key)
        value = urllib.parse.unquote(value)
        
        # Append the (key, value) tuple to the result list
        result.append((key, value))
    
    return result

# Example usage:
qs = "name=John+Doe&age=30&city=New+York&"
print(_parse_qsl(qs))
# Output: [('name', 'John Doe'), ('age', '30'), ('city', 'New York')]
```

### Explanation:
1. **Splitting the Query String**: The query string is split by the `&` character to separate individual key-value pairs.
2. **Handling Empty Segments**: Any empty segments (which can occur if there are trailing `&` characters) are skipped.
3. **Splitting Key-Value Pairs**: Each segment is split by the `=` character to separate the key from the value. If there is no `=`, the entire segment is treated as a key with an empty value.
4. **Replacing `+` with Spaces**: Both keys and values have `+` characters replaced with spaces.
5. **Decoding Percent-Encoded Characters**: The `urllib.parse.unquote` function is used to decode percent-encoded characters in both keys and values.
6. **Storing Results**: The resulting key-value pairs are stored as tuples in a list, which is returned by the function.

This function should handle most typical query strings gracefully, including those with missing values and percent-encoded characters.