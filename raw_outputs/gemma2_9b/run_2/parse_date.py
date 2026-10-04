```python
import base64

def parse_auth(header: str) -> tuple:
    """
    Parses an HTTP Authorization header string.

    Args:
        header (str): The Authorization header string.

    Returns:
        tuple: A tuple containing the authentication scheme and parameters. 
               If the scheme is 'Basic', the tuple is (user, password).
               For other schemes, it's (scheme, parameter). 
               Returns None for malformed or unreadable headers.
    """

    if not isinstance(header, str):
        return None

    parts = header.split(" ", 1)
    if len(parts) != 2:
        return None

    scheme, parameter = parts

    if scheme.lower() == "basic":
        try:
            decoded_data = base64.b64decode(parameter).decode("utf-8")
            user, password = decoded_data.split(":", 1)
            return user, password
        except (base64.binascii.Error, ValueError):
            return None
    else:
        return scheme, parameter 

```

**Explanation:**

1. **Input Check:**
   - The function first checks if the input `header` is a string. If not, it returns `None` as it cannot parse non-string inputs.

2. **Header Splitting:**
   - It splits the `header` string at the first space character using `header.split(" ", 1)`. This separates the scheme (e.g., "Basic") from the parameter (e.g., "..." ).

3. **Scheme and Parameter:**
   - If the split results in exactly two parts, it assigns `scheme` and `parameter` accordingly. Otherwise, it returns `None` indicating a malformed header.

4. **Basic Authentication Handling:**
   - If the `scheme` is "Basic" (case-insensitive), it tries to:
     - Decode the `parameter` using `base64.b64decode`.
     - Decode the resulting bytes to a UTF-8 string.
     - Split the string at the colon (":") to separate the `user` and `password`.
     - Return the `user` and `password` as a tuple.
   - If any error occurs during decoding or splitting (e.g., invalid Base64), it returns `None`.

5. **Other Schemes:**
   - For any other `scheme`, it simply returns the `scheme` and `parameter` as a tuple.

**Important Notes:**

- This function assumes that the Basic authentication payload is always in the format "user:password".
- It does not perform any validation on the user or password. You should add your own validation logic if needed.
- In a real-world application, you would also need to handle potential security issues, such as preventing the storage of passwords in plain text.