Certainly! Below is a Python function `parse_auth` that meets the specified requirements. This function will parse an HTTP Authorization header string, handle the 'Basic' authentication scheme by decoding the payload, and return the appropriate tuples based on the scheme. It will also handle malformed or unreadable headers by returning `None`.

```python
import base64

def parse_auth(header: str) -> tuple:
    if not isinstance(header, str):
        return None
    
    # Split the header into scheme and parameter
    parts = header.split(' ', 1)
    
    if len(parts) != 2:
        return None
    
    scheme, parameter = parts
    
    if scheme.lower() == 'basic':
        try:
            # Decode the base64 encoded parameter
            decoded_bytes = base64.b64decode(parameter)
            decoded_str = decoded_bytes.decode('utf-8')
            user, password = decoded_str.split(':', 1)
            return (user, password)
        except (base64.binascii.Error, UnicodeDecodeError, ValueError):
            return None
    
    return (scheme, parameter)

# Example usage:
# print(parse_auth("Basic QWxhZGRpbjpvcGVuIHNlc2FtZQ=="))  # Output: ('Aladdin', 'open sesame')
# print(parse_auth("Bearer some_token"))                  # Output: ('Bearer', 'some_token')
# print(parse_auth("InvalidHeader"))                      # Output: None
```

### Explanation:
1. **Type Check**: The function first checks if the input `header` is a string. If not, it returns `None`.
2. **Splitting the Header**: The header is split into two parts using `split(' ', 1)`, which splits the string at the first space. This results in a list with two elements: `scheme` and `parameter`.
3. **Validation**: If the split does not result in exactly two parts, the function returns `None`.
4. **Basic Authentication Handling**:
   - If the scheme is 'Basic' (case-insensitive), the function attempts to decode the base64-encoded parameter.
   - It uses `base64.b64decode` to decode the parameter and then decodes the resulting bytes to a UTF-8 string.
   - The decoded string is split at the first colon to separate the `user` and `password`.
   - If any step in this process fails (e.g., base64 decoding error, UTF-8 decoding error, or incorrect format), the function returns `None`.
5. **Other Schemes**: For other schemes, the function simply returns a tuple of the scheme and parameter.

This function should handle the specified cases correctly.