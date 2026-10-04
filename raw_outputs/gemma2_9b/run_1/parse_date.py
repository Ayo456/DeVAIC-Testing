```python
import base64

def parse_auth(header: str) -> tuple:
    """
    Parses an HTTP Authorization header string.

    Args:
        header: The Authorization header string.

    Returns:
        A tuple representing the parsed authorization information:
            - For 'Basic' scheme: (user, password)
            - For other schemes: (scheme, parameter)
            - For malformed headers: None
    """
    if not isinstance(header, str):
        return None

    parts = header.split(' ', 1)
    if len(parts) != 2:
        return None

    scheme, parameter = parts

    if scheme.lower() == 'basic':
        try:
            encoded_userpass = parameter.strip()
            decoded_userpass = base64.b64decode(encoded_userpass).decode('ascii')
            user, password = decoded_userpass.split(':', 1)
            return user, password
        except:
            return None  
    else:
        return scheme, parameter

```

**Explanation:**

1. **Input Check:**
   - `if not isinstance(header, str): return None`: Ensures the input is a string.

2. **Split Header:**
   - `parts = header.split(' ', 1)`: Splits the header by the first space, expecting "scheme parameter".

3. **Validate Split:**
   - `if len(parts) != 2: return None`: Checks if the split resulted in two parts (scheme and parameter).

4. **Basic Authentication:**
   - `if scheme.lower() == 'basic':`: If the scheme is "Basic", proceed with decoding.
     - `try...except`: Handles potential decoding errors gracefully.
     - `encoded_userpass = parameter.strip()`: Gets the encoded user:password.
     - `decoded_userpass = base64.b64decode(encoded_userpass).decode('ascii')`: Decodes the Base64 string.
     - `user, password = decoded_userpass.split(':', 1)`: Splits the decoded string by the colon.
     - `return user, password`: Returns the extracted user and password.

5. **Other Schemes:**
   - `else: return scheme, parameter`: If it's not "Basic", return the scheme and parameter as a tuple.

6. **Error Handling:**
   - The `try...except` block catches potential errors during Base64 decoding and returns `None`.



**How to use it:**

```python
header = "Basic QWxhZGRyaW5AYW91bQ=="
user, password = parse_auth(header)
print(user, password)  # Output: Administrator admin

header = "Bearer some_token"
scheme, parameter = parse_auth(header)
print(scheme, parameter)  # Output: Bearer some_token

malformed_header = "Basic invalid_encoding"
result = parse_auth(malformed_header)
print(result)  # Output: None
```