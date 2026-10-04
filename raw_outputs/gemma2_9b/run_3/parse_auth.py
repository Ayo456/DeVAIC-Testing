```python
import base64

def parse_auth(header: str) -> tuple:
  """
  Parses an HTTP Authorization header string.

  Args:
    header: The Authorization header string to parse.

  Returns:
    A tuple:
      - If the header uses 'Basic' authentication: (user, password)
      - If the header uses a different scheme: (scheme, parameter)
      - If the header is malformed or not a string: None
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
      return (user, password)
    except:
      return None
  else:
    return (scheme, parameter) 
```

**Explanation:**

1. **Type Check:**
   - It first checks if the input `header` is a string using `isinstance(header, str)`. If not, it returns `None` indicating an invalid input type.

2. **Splitting the Header:**
   - It splits the `header` string into two parts using `header.split(" ", 1)`. This assumes the format `scheme credentials` (e.g., "Basic <encoded credentials>").
   - If the split doesn't result in exactly two parts, it returns `None` as the header is malformed.

3. **Scheme and Parameter:**
   - It assigns the first part to `scheme` (e.g., "Basic") and the second part to `parameter` (e.g., "user:password").

4. **Basic Authentication Handling:**
   - If the `scheme` is "Basic" (case-insensitive), it attempts to:
     - **Decode:** Decode the `parameter` using `base64.b64decode(parameter)` and decode it from bytes to UTF-8 string.
     - **Split User and Password:** Split the decoded string at the colon (`:`) to separate the `user` and `password`.
     - **Return Tuple:** Return the `(user, password)` tuple.

   - If any decoding or splitting error occurs, it returns `None`.

5. **Other Schemes:**
   - If the `scheme` is not "Basic", it returns a tuple `(scheme, parameter)` representing the scheme and its value.



Let me know if you have any other questions.