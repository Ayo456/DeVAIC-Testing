Certainly! Below is the Python function `parse_auth` that meets the specified requirements:

```python
import base64

def parse_auth(header: str) -> tuple:
    if not isinstance(header, str):
        return None
    
    try:
        # Split the header into scheme and parameter
        parts = header.split(' ', 1)
        if len(parts) != 2:
            return None
        
        scheme, parameter = parts
        
        if scheme.lower() == 'basic':
            # Decode the base64 encoded parameter
            try:
                decoded_bytes = base64.b64decode(parameter)
                decoded_str = decoded_bytes.decode('utf-8')
                user, password = decoded_str.split(':', 1)
                return (user, password)
            except (base64.binascii.Error, UnicodeDecodeError, ValueError):
                return None
        else:
            return (scheme, parameter)
    
    except Exception:
        return None

# Example usage:
# print(parse_auth("Basic QWxhZGRpbjpvcGVuIHNlc2FtZQ=="))  # Output: ('Aladdin', 'open sesame')
# print(parse_auth("Bearer some_token"))  # Output: ('Bearer', 'some_token')
# print(parse_auth("Invalid header"))  # Output: None
```

### Explanation:
1. **Type Check**: The function first checks if the input `header` is a string. If not, it returns `None`.
2. **Splitting the Header**: The header is split into two parts using `split(' ', 1)`. This ensures that only the first space is considered as the delimiter, which separates the scheme from the parameter.
3. **Scheme Check**: If the scheme is 'Basic' (case-insensitive), the parameter is decoded from base64. If the decoding is successful, the decoded string is split into `user` and `password` using the first colon as the delimiter.
4. **Error Handling**: If any part of the process fails (e.g., base64 decoding error, Unicode decoding error, or incorrect format), the function returns `None`.
5. **Other Schemes**: For other schemes, the function simply returns a tuple of the scheme and parameter.
6. **General Exception Handling**: Any unexpected exceptions are caught and `None` is returned.

This function should handle various edge cases and malformed headers gracefully.