Certainly! Below is the implementation of the `parse_auth` function that meets the specified requirements:

```python
import base64

def parse_auth(header: str) -> tuple:
    if not isinstance(header, str):
        return None
    
    parts = header.split(' ', 1)
    if len(parts) != 2:
        return None
    
    scheme, parameter = parts
    
    if scheme.lower() == 'basic':
        try:
            decoded_bytes = base64.b64decode(parameter)
            decoded_str = decoded_bytes.decode('utf-8')
            user, password = decoded_str.split(':', 1)
            return (user, password)
        except (base64.binascii.Error, UnicodeDecodeError, ValueError):
            return None
    
    return (scheme, parameter)

# Example usage:
# print(parse_auth("Basic QWxhZGRpbjpvcGVuIHNlc2FtZQ=="))  # Output: ('Aladdin', 'open sesame')
# print(parse_auth("Bearer some_token"))  # Output: ('Bearer', 'some_token')
# print(parse_auth("InvalidHeader"))  # Output: None
```

### Explanation:
1. **Type Check**: The function first checks if the input `header` is a string. If not, it returns `None`.
2. **Split Header**: The header string is split into two parts using the first space character. This separates the scheme from the parameter.
3. **Malformed Check**: If the split does not result in exactly two parts, the function returns `None`.
4. **Basic Scheme Handling**:
   - If the scheme is 'Basic' (case-insensitive), the function attempts to decode the base64-encoded parameter.
   - The decoded string is then split into `user` and `password` using the first colon.
   - If any step in this process fails (decoding, decoding to string, splitting), the function returns `None`.
5. **Other Schemes**: For other schemes, the function returns a tuple of the scheme and parameter.

This function ensures that only well-formed and supported headers are processed, and it handles errors gracefully by returning `None` for malformed or unsupported cases.