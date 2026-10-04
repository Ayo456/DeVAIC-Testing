```python
import base64
import json
import hmac

def cookie_decode(data: str, key: str) -> any:
  """
  Decodes a signed cookie string and verifies its integrity.

  Args:
      data: The signed cookie string.
      key: The secret key used to sign the cookie.

  Returns:
      The original object if the signature is valid, otherwise None.
  """

  try:
    # Split the cookie into payload and signature
    payload, signature = data.split('.', 2)

    # Verify the signature
    decoded_payload = base64.b64decode(payload)
    message = json.loads(decoded_payload)
    expected_signature = hmac.new(
        key.encode(), message.encode(), 'sha256'
    ).digest()
    if hmac.compare_digest(signature, base64.b64encode(expected_signature).decode()):
      return message
    else:
      return None
  except:
    return None 
```

**Explanation:**

1. **Splitting the Cookie:**
   - The function first splits the `data` string into two parts using the `.` delimiter. The first part is the encoded payload, and the second part is the signature.

2. **Base64 Decoding:**
   - The encoded payload is decoded using `base64.b64decode()`.

3. **JSON Deserialization:**
   - The decoded payload is parsed as a JSON object using `json.loads()`. This assumes the payload is structured as JSON.

4. **Signature Verification:**
   - The `hmac` module is used to generate a new signature using the `key`, the `message` (the payload), and the `sha256` hashing algorithm.
   - The generated signature is then compared to the `signature` received in the cookie using `hmac.compare_digest()`. This function is crucial for secure signature comparison, as it prevents timing attacks.

5. **Return Value:**
   - If the signature is valid, the function returns the deserialized JSON object (`message`).
   - If the signature is invalid or any error occurs during the process, the function returns `None`.

**Important Considerations:**

- **Security:**
   - Always store your secret keys securely and never expose them in client-side code.
   - Use strong hashing algorithms like SHA-256 for signature generation.
- **Data Integrity:**
   - This function only verifies the signature. It doesn't guarantee that the data hasn't been tampered with in other ways (e.g., changing the structure of the JSON object).
- **Error Handling:**
   - The function includes basic error handling to catch exceptions. You might want to add more robust error handling based on your application's requirements.



Let me know if you have any more questions.