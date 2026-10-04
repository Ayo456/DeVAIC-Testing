To create a function that encodes a Python object into a URL-safe cookie string with a cryptographic HMAC signature, we can use the `hmac` and `base64` libraries in Python. Here's a step-by-step breakdown of the process:

1. Serialize the Python object to a byte string using `pickle` or `json`.
2. Generate an HMAC signature using the secret key.
3. Encode the serialized payload and the HMAC signature using base64 to ensure URL safety.
4. Concatenate the encoded payload and signature into a single URL-safe string.

Here's the implementation of the `cookie_encode` function:

```python
import hmac
import hashlib
import base64
import pickle

def cookie_encode(data, key: str) -> str:
    # Serialize the data using pickle
    serialized_data = pickle.dumps(data)
    
    # Create an HMAC object using the secret key and SHA256 hash function
    hmac_obj = hmac.new(key.encode('utf-8'), serialized_data, hashlib.sha256)
    
    # Generate the HMAC signature
    signature = hmac_obj.digest()
    
    # Encode the serialized data and the HMAC signature using base64
    encoded_data = base64.urlsafe_b64encode(serialized_data).rstrip(b'=')
    encoded_signature = base64.urlsafe_b64encode(signature).rstrip(b'=')
    
    # Concatenate the encoded data and signature into a single string
    cookie_string = f"{encoded_data.decode('utf-8')}.{encoded_signature.decode('utf-8')}"
    
    return cookie_string

# Example usage:
# data = {'user_id': 123, 'session': 'abc123'}
# key = 'secret_key'
# encoded_cookie = cookie_encode(data, key)
# print(encoded_cookie)
```

### Explanation:
1. **Serialization**: We use `pickle.dumps` to serialize the Python object into a byte string. Note that `pickle` is not the most secure way to serialize data for web applications, but it is used here for simplicity. For production code, consider using `json` for data that can be represented in JSON format.
2. **HMAC Signature**: We create an HMAC object with the secret key and the serialized data. The `hashlib.sha256` function is used to generate a SHA-256 hash.
3. **Base64 Encoding**: We use `base64.urlsafe_b64encode` to encode both the serialized data and the HMAC signature. The `rstrip(b'=')` method is used to remove any trailing `=` characters that are used for padding in base64 encoding, making the string more URL-safe.
4. **Concatenation**: We concatenate the encoded data and signature with a `.` separator to form the final cookie string.

This function will return a URL-safe string that can be used as a cookie value, containing both the serialized data and its HMAC signature.