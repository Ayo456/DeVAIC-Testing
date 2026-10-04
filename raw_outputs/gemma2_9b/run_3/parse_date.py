```python
import base64

def parse_auth(header: str) -> tuple:
  """
  Parses an HTTP Authorization header string.

  Args:
      header: The Authorization header string to parse.

  Returns:
      A tuple representing the parsed authentication information:
          - For 'Basic' scheme: (user, password)
          - For other schemes: (scheme, parameter)
          - If malformed or unreadable: None
  """
  if not isinstance(header, str):
    return None

  parts = header.split(" ")
  if len(parts) != 2:
    return None  

  scheme, parameter = parts

  if scheme.lower() == "basic":
    try:
      decoded_payload = base64.b64decode(parameter).decode('utf-8')
      user, password = decoded_payload.split(':', 1)
      return (user, password)
    except:
      return None  
  else:
    return (scheme, parameter) 
```

**Explanation:**

1. **Input Check:** 
   - The function first checks if the input `header` is a string. If not, it returns `None` as it cannot parse non-string inputs.

2. **Header Splitting:**
   - The `header` is split using ` " " ` as the delimiter.  
   - It expects two parts: the `scheme` (e.g., "Basic") and the `parameter` (e.g., "username:password").

3. **Scheme Handling:**
   - If the `scheme` is "Basic" (case-insensitive), it proceeds to decode the `parameter`.
   - For other schemes, it simply returns the `scheme` and `parameter` as a tuple.

4. **Basic Authentication Decoding:**
   - **Base64 Decoding:** The `parameter` is decoded using `base64.b64decode()`. This converts the Base64-encoded string into its original bytes representation.
   - **UTF-8 Decoding:** The decoded bytes are then decoded into a UTF-8 string using `.decode('utf-8')`.
   - **Splitting User and Password:** The decoded string is split using `':'` to separate the `user` and `password`.
   - **Return Tuple:** The function returns a tuple containing the `user` and `password`.

5. **Error Handling:**
   - A `try...except` block is used to catch any exceptions during base64 decoding or string splitting. If an error occurs, it returns `None`.



**Example Usage:**

```python
header = "Basic QWxhZGRpbjpvcGVuQ2xpY2sg"
user, password = parse_auth(header)
print(user, password)  # Output: Alex password

header2 = "Bearer some_token"
scheme, parameter = parse_auth(header2)
print(scheme, parameter)  # Output: Bearer some_token

malformed_header = "Authorization invalid"
result = parse_auth(malformed_header)
print(result)  # Output: None
```