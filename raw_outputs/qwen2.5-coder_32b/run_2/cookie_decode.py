To implement the `cookie_decode` function, we need to understand how signed cookies are typically encoded and decoded. A common approach is to use HMAC (Hash-based Message Authentication Code) to sign the cookie data. The cookie string usually consists of the base64-encoded payload and the signature, separated by a delimiter.

Here's a step-by-step breakdown of how to implement this:

1. **Split the cookie string**: Separate the base64-encoded payload from the signature.
2. **Decode the payload**: Convert the base64-encoded payload back to its original form.
3. **Verify the signature**: Use HMAC to verify that the signature matches the payload and key.
4. **Deserialize the payload**: Convert the payload back to its original object (usually a dictionary).
5. **Return the object or None**: If the signature is valid, return the deserialized object; otherwise, return `None`.

Below is the implementation of the `cookie_decode` function:

```python
import base64
import hmac
import hashlib
import pickle

def cookie_decode(data: str, key: str) -> object:
    # Split the data into payload and signature
    parts = data.split('.')
    if len(parts) != 2:
        return None
    
    encoded_payload, signature = parts
    
    # Decode the payload
    try:
        payload = base64.urlsafe_b64decode(encoded_payload + '==')
    except Exception:
        return None
    
    # Compute the expected signature
    expected_signature = hmac.new(key.encode(), payload, hashlib.sha256).hexdigest()
    
    # Compare the provided signature with the expected one
    if not hmac.compare_digest(signature, expected_signature):
        return None
    
    # Deserialize the payload
    try:
        obj = pickle.loads(payload)
    except Exception:
        return None
    
    return obj

# Example usage:
# signed_cookie = 'base64_encoded_payload.signature'
# secret_key = 'your_secret_key'
# result = cookie_decode(signed_cookie, secret_key)
```

### Important Notes:
1. **Security**: Using `pickle` for deserialization can be dangerous if the data is not trusted, as it can execute arbitrary code. Ensure that the data comes from a trusted source or consider using a safer serialization format like JSON.
2. **Base64 Padding**: The `base64.urlsafe_b64decode` function requires the input to be padded to a multiple of 4 bytes. Adding '==' ensures that this requirement is met.
3. **HMAC**: The `hmac.compare_digest` function is used to compare the signatures in a way that is resistant to timing attacks.

This function assumes that the cookie data is formatted as `base64_encoded_payload.signature` and that the signature is computed using HMAC-SHA256. Adjust the implementation if your specific use case differs.