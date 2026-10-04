Certainly! Below is the implementation of the `parse_auth` function that meets the specified requirements:

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
            # Decode the Base64 encoded parameter
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
# print(parse_auth("Basic dXNlcjpwYXNzd29yZA=="))  # Output: ('user', 'password')
# print(parse_auth("Bearer some_token"))           # Output: ('Bearer', 'some_token')
# print(parse_auth("InvalidHeader"))               # Output: None
```

### Explanation:
1. **Type Check**: The function first checks if the input `header` is a string. If not, it returns `None`.
2. **Splitting the Header**: The header is split into two parts using the space character as a delimiter. If the split does not result in exactly two parts, it returns `None`.
3. **Scheme Handling**:
   - If the scheme is `Basic` (case-insensitive), it decodes the Base64 encoded parameter.
     - It uses `base64.b64decode` to decode the parameter.
     - It then decodes the resulting bytes to a string and splits it into `user` and `password` using the colon `:` as a delimiter.
     - If any step in this process fails (e.g., invalid Base64, decoding error, or incorrect format), it returns `None`.
   - For other schemes, it returns a tuple containing the scheme and the parameter.
4. **Exception Handling**: Any unexpected exceptions during the parsing process result in `None` being returned.

This function should handle the specified cases and edge cases effectively.