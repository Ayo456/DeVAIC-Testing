Certainly! Below is a Python function named `parse_auth` that meets the specified requirements:

```python
import base64
import re

def parse_auth(header: str) -> tuple:
    if not isinstance(header, str):
        return None
    
    # Regular expression to match the Authorization header format
    auth_pattern = re.compile(r'^(\w+)\s+(\S+)$')
    match = auth_pattern.match(header)
    
    if not match:
        return None
    
    scheme = match.group(1)
    parameter = match.group(2)
    
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
# print(parse_auth("Basic dXNlcjpwYXNzd29yZA=="))  # Output: ('user', 'password')
# print(parse_auth("Bearer some_token"))          # Output: ('Bearer', 'some_token')
# print(parse_auth("Invalid header"))             # Output: None
```

### Explanation:
1. **Type Check**: The function first checks if the input `header` is a string. If not, it returns `None`.
2. **Regular Expression**: It uses a regular expression to match the format of the Authorization header. The pattern `^(\w+)\s+(\S+)$` ensures that the header starts with a word (the scheme), followed by one or more whitespace characters, and then a non-whitespace string (the parameter).
3. **Match and Extract**: If the header matches the pattern, it extracts the `scheme` and `parameter`.
4. **Basic Authentication Handling**: If the scheme is 'Basic', it attempts to decode the base64-encoded parameter. It splits the decoded string at the first colon to separate the user and password. If any step in this process fails (e.g., decoding error, splitting error), it returns `None`.
5. **Other Schemes**: For other schemes, it simply returns the tuple `(scheme, parameter)`.
6. **Malformed Headers**: If the header does not match the expected format, it returns `None`.

This function should handle various edge cases and malformed headers gracefully.