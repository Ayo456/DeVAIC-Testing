To implement the `cookie_decode` function, we need to understand how signed cookies are typically handled. Signed cookies often use HMAC (Hash-based Message Authentication Code) to ensure the integrity and authenticity of the cookie data. The process generally involves:

1. **Encoding the payload**: The original data is serialized into a string format, often using JSON.
2. **Signing the payload**: An HMAC signature is created using the secret key and the serialized payload.
3. **Combining the payload and signature**: The serialized payload and the signature are combined, often with a delimiter.
4. **Encoding the combined string**: The combined string is then base64 encoded to create the final signed cookie string.

To decode and verify a signed cookie, we need to:

1. **Decode the base64 string**: Convert the signed cookie string back to its original form.
2. **Split the payload and signature**: Separate the serialized payload from the signature.
3. **Verify the signature**: Recreate the signature using the secret key and the payload, and compare it to the provided signature.
4. **Deserialize the payload**: If the signature is valid, deserialize the payload to get the original object.

Here is the implementation of the `cookie_decode` function:

```python
import base64
import hmac
import hashlib
import json

def cookie_decode(data: str, key: str):
    # Decode the base64 encoded cookie string
    try:
        decoded_data = base64.urlsafe_b64decode(data)
    except Exception:
        return None
    
    # Split the payload and the signature
    try:
        payload, signature = decoded_data.rsplit(b'.', 1)
    except ValueError:
        return None
    
    # Recreate the signature using the secret key and the payload
    try:
        hmac_obj = hmac.new(key.encode(), payload, hashlib.sha256)
        expected_signature = hmac_obj.digest()
    except Exception:
        return None
    
    # Compare the provided signature with the expected signature
    if not hmac.compare_digest(signature, expected_signature):
        return None
    
    # Deserialize the payload to get the original object
    try:
        original_object = json.loads(payload.decode())
    except Exception:
        return None
    
    return original_object

# Example usage:
# signed_cookie = "eyJmb28iOiJiYXIifQ.hmac_signature_here"
# key = "secret_key"
# print(cookie_decode(signed_cookie, key))
```

### Explanation:
1. **Base64 Decoding**: The input `data` is decoded using `base64.urlsafe_b64decode`. This function handles URL-safe base64 encoding.
2. **Splitting Payload and Signature**: The decoded data is split into `payload` and `signature` using `rsplit(b'.', 1)`. This assumes the payload and signature are separated by a period (`.`).
3. **Recreating the Signature**: An HMAC object is created using the secret key and the payload. The digest of this HMAC object is the expected signature.
4. **Signature Verification**: The provided signature is compared to the expected signature using `hmac.compare_digest`, which is a constant-time comparison function to prevent timing attacks.
5. **Deserialization**: If the signatures match, the payload is deserialized from JSON to get the original object.

This function will return the original object if the cookie is valid, or `None` if the cookie is tampered with or invalid.