```python
import base64

def parse_auth(header: str) -> tuple:
  """
  Parses an HTTP Authorization header string.

  Args:
    header: The Authorization header string.

  Returns:
    A tuple containing the authentication scheme and parameter. 
    For 'Basic' scheme, returns (user, password). 
    For other schemes, returns (scheme, parameter). 
    Returns None for malformed or unreadable headers.
  """
  if not isinstance(header, str):
    return None

  parts = header.strip().split(' ', 1)
  if len(parts) != 2:
    return None

  scheme, parameter = parts

  if scheme.lower() == 'basic':
    try:
      decoded_parameter = base64.b64decode(parameter).decode('ascii')
      user, password = decoded_parameter.split(':', 1)
      return (user, password)
    except:
      return None
  else:
    return (scheme, parameter) 
```

**Explanation:**

1. **Type Check:** The function first checks if the input `header` is a string using `isinstance(header, str)`. If not, it returns `None` as it cannot process non-string inputs.

2. **Splitting the Header:** The header string is split into two parts based on the space character using `header.strip().split(' ', 1)`. 
   - `strip()` removes leading and trailing whitespaces.
   - `split(' ', 1)` splits the string at the first space, limiting the split to one occurrence.
   - If the split doesn't result in two parts, it indicates a malformed header, so `None` is returned.

3. **Scheme and Parameter:** The two parts obtained from the split are assigned to the `scheme` and `parameter` variables.

4. **Basic Authentication:**
   - If the `scheme` (converted to lowercase) is "basic":
     - The `parameter` is base64 decoded using `base64.b64decode(parameter)`. 
     - The decoded string is then decoded from bytes to ASCII string using `decode('ascii')`.
     - The decoded string is split at the colon (`:`) to separate the `user` and `password`.
     - The function returns a tuple `(user, password)`.
   - If any decoding or splitting error occurs, `None` is returned.

5. **Other Schemes:**
   - If the `scheme` is not "basic", the function returns a tuple `(scheme, parameter)` as is.


**Example Usage:**

```python
header = "Basic QWxhZGRpbjpvcGVuc2Vj"
user, password = parse_auth(header)
print(f"User: {user}, Password: {password}")  # Output: User: John, Password: Doe

header = "Bearer token123"
scheme, parameter = parse_auth(header)
print(f"Scheme: {scheme}, Parameter: {parameter}")  # Output: Scheme: Bearer, Parameter: token123

malformed_header = "Basic invalid"
result = parse_auth(malformed_header)
print(result)  # Output: None
```