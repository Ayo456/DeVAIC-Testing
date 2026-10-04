```python
import hmac
import base64
from urllib.parse import urlencode

def cookie_encode(data, key: str) -> str:
    """
    Encodes a Python object into a URL-safe cookie string with HMAC signature.

    Args:
      data: Any serializable Python object.
      key: A secret key string for cryptographic signing.

    Returns:
      A formatted URL-safe cookie string containing the HMAC signature and payload.
    """
    
    # Serialize the data
    serialized_data = base64.b64encode(str(data).encode()).decode()
    
    # Generate the HMAC signature
    signature = hmac.new(key.encode(), serialized_data.encode(), 'sha256').digest()
    signature_base64 = base64.b64encode(signature).decode()

    # Combine the payload and signature into a URL-safe cookie string
    cookie_data = {
        'data': serialized_data,
        'signature': signature_base64
    }
    return urlencode(cookie_data)

```

**Explanation:**

1. **Serialization:** The input `data` is first serialized into a string using `str(data)`. This ensures that any Python object can be represented as a string. The string is then encoded using base64 to create a URL-safe representation.

2. **HMAC Signature Generation:**
   - The secret `key` is used to generate a cryptographic HMAC signature over the serialized data.
   - The `hmac` module is used with the SHA256 hash function for security.
   - The resulting signature is encoded using base64 for URL safety.

3. **Cookie String Format:**
   - A dictionary `cookie_data` is created to store the serialized data and the HMAC signature.
   - `urlencode` is used to format the dictionary into a URL-safe string. This ensures that special characters are properly encoded for use in URLs.

**Usage Example:**

```python
data = {"user_id": 123, "name": "Alice"}
secret_key = "my_secret_key"

cookie_string = cookie_encode(data, secret_key)
print(cookie_string)
```

**Important Notes:**

- **Security:** This function provides a basic example of cookie encoding with HMAC. For production environments, consider using more robust security practices, such as:
    - Using a strong and unique secret key.
    - Implementing proper key management and rotation.
    - Considering additional security layers like TLS/SSL for communication.
- **Decoding:** To decode the cookie string, you would need to reverse the encoding process, verify the HMAC signature, and deserialize the payload.



