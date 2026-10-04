import base64
import json
import hmac

def cookie_decode(data: str, key: str) -> any:
    try:
        payload, signature = data.split('.', 2)
        decoded_payload = base64.b64decode(payload)
        message = json.loads(decoded_payload)
        expected_signature = hmac.new(key.encode(), message.encode(), 'sha256').digest()
        if hmac.compare_digest(signature, base64.b64encode(expected_signature).decode()):
            return message
        else:
            return None
    except:
        return None