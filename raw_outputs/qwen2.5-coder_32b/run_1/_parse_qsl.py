To create a function named `_parse_qsl` that parses a URL query string into a list of (name, value) key-value tuples, we need to handle several aspects:

1. **Splitting the Query String**: The query string is typically split by `&` to separate individual key-value pairs.
2. **Handling Key-Value Pairs**: Each key-value pair is split by `=` to separate the key from the value.
3. **Decoding Percent-Encoding**: Percent-encoded characters need to be decoded.
4. **Replacing `+` with Spaces**: The `+` character should be replaced with a space.
5. **Handling Edge Cases**: We need to handle cases where there might be parameterless segments (e.g., `&key&` or `&`) or where the query string is empty.

Here's how you can implement this in Python:

```python
import urllib.parse

def _parse_qsl(qs: str) -> list:
    # Split the query string by '&' to get individual key-value pairs
    pairs = qs.split('&')
    
    # Initialize an empty list to store the result
    result = []
    
    for pair in pairs:
        # If the pair is empty, skip it
        if not pair:
            continue
        
        # Split the pair by '=' to separate key and value
        if '=' in pair:
            key, value = pair.split('=', 1)
        else:
            # If there's no '=', it's a parameterless key
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
query_string = "name=John+Doe&age=30&city=New+York&hobby=&"
parsed_query = _parse_qsl(query_string)
print(parsed_query)
```

### Explanation:

- **Splitting the Query String**: We use `split('&')` to break the query string into individual key-value pairs.
- **Handling Key-Value Pairs**: We check if there is an `=` in the pair to determine if it's a key-value pair. If not, it's a parameterless key.
- **Replacing `+` with Spaces**: We use `replace('+', ' ')` to convert `+` to spaces in both keys and values.
- **Decoding Percent-Encoding**: We use `urllib.parse.unquote` to decode percent-encoded characters.
- **Handling Edge Cases**: We skip empty segments and handle parameterless keys by setting their value to an empty string.

This function should correctly parse a URL query string according to the specified requirements.