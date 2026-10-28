import base64
from hashlib import hmac

def cookie_decode(data, key):
    if isinstance(data, str):
        data = data.encode()
    parts = data.split(b'?', 1)
    if len(parts) != 2:
        return None
    signature, message = parts
    try:
        decoded_message = base64.b64decode(message)
    except:
        return None
    computed_signature = hmac(key.encode(), decoded_message, 'sha256').digest()
    try:
        return base64.b64decode(signature).hex() == hmac(key.encode(), decoded_message, 'sha256').hexdigest()
    except:
        return None