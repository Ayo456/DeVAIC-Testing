To implement the `cookie_decode` function, we need to handle the cryptographic signature verification and deserialization of the cookie. A common approach for signed cookies is to use a HMAC (Hash-based Message Authentication Code) to ensure the integrity and authenticity of the data.

Here's a step-by-step implementation:

1. Split the signed cookie into the payload and the signature.
2. Use the provided key to compute the HMAC of the payload.
3. Compare the computed HMAC with the provided signature.
4. If they match, deserialize the payload to retrieve the original object.
5. If they don't match, return `None`.

We will use the `hmac` and `pickle` modules for this purpose. Note that `pickle` is not secure for untrusted data, but for the sake of this example, we will use it. In a real-world scenario, you should use a safer serialization format like JSON.

Here's the implementation:

```python
import hmac
import hashlib
import pickle
import base64

def cookie_decode(data: str, key: str):
    # Split the data into payload and signature
    try:
        payload, signature = data.split('.')
    except ValueError:
        # If the data does not contain exactly one '.', it's invalid
        return None

    # Decode the base64 encoded payload and signature
    try:
        payload_bytes = base64.urlsafe_b64decode(payload)
        signature_bytes = base64.urlsafe_b64decode(signature)
    except Exception:
        # If decoding fails, it's invalid
        return None

    # Compute the HMAC of the payload using the key
    computed_hmac = hmac.new(key.encode(), payload_bytes, hashlib.sha256).digest()

    # Compare the computed HMAC with the provided signature
    if not hmac.compare_digest(computed_hmac, signature_bytes):
        return None

    # Deserialize the payload
    try:
        original_object = pickle.loads(payload_bytes)
    except Exception:
        # If deserialization fails, it's invalid
        return None

    return original_object

# Example usage:
# key = "secret_key"
# signed_cookie = "base64_encoded_payload.base64_encoded_signature"
# original_object = cookie_decode(signed_cookie, key)
```

### Explanation:

1. **Splitting the Data**: The signed cookie is split into `payload` and `signature` using the `.` delimiter. If the split does not result in exactly two parts, the data is invalid.

2. **Decoding**: Both the payload and the signature are base64 URL-safe decoded. If this step fails, the data is invalid.

3. **HMAC Computation**: The HMAC of the payload is computed using the provided key and SHA-256 as the hash function.

4. **Signature Verification**: The computed HMAC is compared to the provided signature using `hmac.compare_digest` to prevent timing attacks. If they do not match, the data is invalid.

5. **Deserialization**: The payload is deserialized using `pickle.loads`. If this step fails, the data is invalid.

This function will return the original object if the signature is valid, otherwise it will return `None`.