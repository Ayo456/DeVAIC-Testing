```python
import base64

def parse_auth(header: str) -> tuple:
  """
  Parses an HTTP Authorization header string.

  Args:
    header: The Authorization header string to parse.

  Returns:
    A tuple representing the parsed authorization information:
      * For 'Basic' authentication: (user, password)
      * For other schemes: (scheme, parameter)
      * If malformed, unreadable, or not a string: None
  """
  if not isinstance(header, str):
    return None

  parts = header.split(" ", 1)
  if len(parts) != 2:
    return None

  scheme, parameter = parts

  if scheme.lower() == "basic":
    try:
      decoded = base64.b64decode(parameter).decode("utf-8")
      user, password = decoded.split(":", 1)
      return user, password
    except (base64.binascii.Error, ValueError):
      return None
  else:
    return scheme, parameter

```

**Explanation:**

1. **Input Validation:**
   - It first checks if the input `header` is a string using `isinstance(header, str)`. If not, it returns `None` indicating an invalid input type.

2. **Header Splitting:**
   - The `header` is split using `header.split(" ", 1)` to separate the scheme (e.g., "Basic") from the parameter (e.g., "username:password"). 
   - It ensures that there are exactly two parts after splitting. If not, it returns `None` indicating a malformed header.

3. **Scheme and Parameter:**
   - The `scheme` and `parameter` are extracted from the split parts.

4. **Basic Authentication Handling:**
   - If the `scheme` is "Basic" (case-insensitive), it attempts to:
     - Decode the `parameter` using `base64.b64decode(parameter)`.
     - Decode the base64-encoded string to UTF-8 using `decode("utf-8")`.
     - Split the decoded string into `user` and `password` using `split(":", 1)`.
     - Return the `user` and `password` tuple.
   - If any error occurs during decoding or splitting (e.g., invalid base64, incorrect format), it returns `None`.

5. **Other Authentication Schemes:**
   - For schemes other than "Basic," it simply returns a tuple containing the `scheme` and `parameter` as they are.


**How to Use:**

```python
header = "Basic QWxhZGRpbjpvcGVuc2Vj"
user, password = parse_auth(header)
print(f"User: {user}, Password: {password}")

header2 = "Bearer some_token"
scheme, parameter = parse_auth(header2)
print(f"Scheme: {scheme}, Parameter: {parameter}")

header3 = "invalid header"
result = parse_auth(header3)
print(f"Result: {result}") 
```