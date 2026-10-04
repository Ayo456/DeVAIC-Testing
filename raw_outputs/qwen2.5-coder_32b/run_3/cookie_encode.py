To create a function `cookie_encode` that serializes a Python object, generates a HMAC signature, and returns a URL-safe cookie string, we can use the `pickle` module for serialization, `hmac` for generating the HMAC signature, and `base64` for URL-safe encoding. Here's how you can implement this:

1. **Serialization**: Use `pickle.dumps` to serialize the Python object.
2. **HMAC Signature**: Use `hmac.new` to create a HMAC object with the provided key and the serialized data.
3. **Encoding**: Use `base64.urlsafe_b64encode` to encode both the serialized data and the HMAC signature to make them URL-safe.

Here's the complete implementation:

```python
import pickle
import hmac
import hashlib
import base64

def cookie_encode(data, key: str) -> str:
    # Serialize the data
    serialized_data = pickle.dumps(data)
    
    # Create a HMAC object using the key and the serialized data
    hmac_obj = hmac.new(key.encode(), serialized_data, hashlib.sha256)
    
    # Generate the HMAC signature
    signature = hmac_obj.digest()
    
    # Encode the serialized data and the signature in a URL-safe way
    encoded_data = base64.urlsafe_b64encode(serialized_data).rstrip(b'=')
    encoded_signature = base64.urlsafe_b64encode(signature).rstrip(b'=')
    
    # Combine the signature and the data into a single URL-safe string
    cookie_string = f"{encoded_signature}.{encoded_data}"
    
    return cookie_string

# Example usage:
# data = {"user_id": 123, "username": "example_user"}
# key = "secret_key"
# cookie = cookie_encode(data, key)
# print(cookie)
```

### Explanation:
1. **Serialization**: `pickle.dumps(data)` converts the Python object `data` into a byte stream.
2. **HMAC Signature**: `hmac.new(key.encode(), serialized_data, hashlib.sha256)` creates a new HMAC object using the key and the serialized data, with SHA256 as the hash function.
3. **Encoding**: `base64.urlsafe_b64encode` encodes the serialized data and the HMAC signature in a URL-safe manner. The `rstrip(b'=')` is used to remove any trailing `=` characters which are safe to remove in URL-safe base64 encoding.
4. **Combining**: The encoded signature and data are combined with a `.` separator to form the final cookie string.

### Security Note:
- **Pickle Security**: Be cautious when using `pickle` for serialization, as it can execute arbitrary code during deserialization. Ensure that the data being deserialized is trusted.
- **Key Management**: Ensure that the secret key is kept secure and is not hard-coded in the source code. Use environment variables or secure vaults for managing keys.

This function will generate a URL-safe cookie string that includes both the serialized data and its HMAC signature, which can be used for secure cookie-based storage or transmission.