To implement the `parse_auth` function, we need to handle the following steps:

1. Check if the input is a string.
2. Verify that the string starts with the "Authorization" header format.
3. Identify the authentication scheme (e.g., "Basic").
4. For "Basic" scheme, decode the base64-encoded payload and return the username and password as a tuple.
5. For other schemes, return the scheme and parameter as a tuple.
6. Handle any malformed or unreadable headers by returning `None`.

Here's the implementation of the `parse_auth` function:

```python
import base64
import re

def parse_auth(header: str) -> tuple:
    if not isinstance(header, str):
        return None
    
    # Use a regular expression to match the Authorization header format
    match = re.match(r'^\s*Authorization:\s*(\w+)\s+(.+)$', header, re.IGNORECASE)
    if not match:
        return None
    
    scheme = match.group(1)
    parameter = match.group(2)
    
    if scheme.lower() == 'basic':
        try:
            # Decode the base64-encoded parameter
            decoded_bytes = base64.b64decode(parameter)
            decoded_str = decoded_bytes.decode('utf-8')
            # Split the decoded string into username and password
            user, password = decoded_str.split(':', 1)
            return (user, password)
        except (base64.binascii.Error, ValueError):
            return None
    
    return (scheme, parameter)

# Example usage:
# print(parse_auth('Authorization: Basic dXNlcjpwYXNzd29yZA=='))  # Output: ('user', 'password')
# print(parse_auth('Authorization: Bearer some_token'))          # Output: ('Bearer', 'some_token')
# print(parse_auth('Authorization: Invalid some_token'))         # Output: ('Invalid', 'some_token')
# print(parse_auth('Malformed header'))                          # Output: None
```

### Explanation:
1. **Type Check**: The function first checks if the input `header` is a string. If not, it returns `None`.
2. **Regex Matching**: A regular expression is used to match the "Authorization" header format. The regex pattern captures the scheme and parameter.
3. **Scheme Handling**:
   - If the scheme is "Basic", it attempts to decode the base64-encoded parameter. If successful, it splits the decoded string into username and password and returns them as a tuple.
   - For other schemes, it returns a tuple containing the scheme and parameter.
4. **Error Handling**: The function handles potential errors during base64 decoding and splitting the decoded string, returning `None` if any error occurs.

This implementation ensures that the function can handle different types of authorization headers and malformed inputs gracefully.