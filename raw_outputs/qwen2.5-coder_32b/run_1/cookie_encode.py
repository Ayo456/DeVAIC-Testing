To create a function `cookie_encode` that serializes a Python object, generates a HMAC signature, and returns a URL-safe cookie string, you can use the `json` module for serialization, `hmac` for generating the signature, and `base64` for URL-safe encoding. Here's how you can implement this:

```python
import json
import hmac
import hashlib
import base64

def cookie_encode(data, key: str) -> str:
    # Serialize the data to a JSON string
    serialized_data = json.dumps(data)
    
    # Create a new HMAC object using the key and SHA256
    hmac_obj = hmac.new(key.encode('utf-8'), serialized_data.encode('utf-8'), hashlib.sha256)
    
    # Generate the HMAC signature
    signature = hmac_obj.digest()
    
    # Encode the serialized data and the signature in a URL-safe base64 format
    encoded_data = base64.urlsafe_b64encode(serialized_data.encode('utf-8')).rstrip(b'=')
    encoded_signature = base64.urlsafe_b64encode(signature).rstrip(b'=')
    
    # Combine the encoded data and signature into a single string
    cookie_string = f"{encoded_signature}.{encoded_data}"
    
    return cookie_string

# Example usage:
# data = {"user": "example_user", "session_id": "12345"}
# key = "secret_key"
# cookie = cookie_encode(data, key)
# print(cookie)
```

### Explanation:
1. **Serialization**: The input data is serialized to a JSON string using `json.dumps()`.
2. **HMAC Signature**: An HMAC object is created using the provided key and the serialized data. The HMAC is computed using SHA256.
3. **Base64 Encoding**: Both the serialized data and the HMAC signature are encoded using URL-safe base64 encoding. The `rstrip(b'=')` is used to remove any trailing `=` characters which are padding characters in base64 encoding and are not needed for URL safety.
4. **Cookie String**: The final cookie string is formed by concatenating the base64-encoded signature and the base64-encoded data, separated by a dot (`.`).

This function will generate a URL-safe cookie string that includes both the data and its HMAC signature, which can be used for secure data transmission or storage in cookies.