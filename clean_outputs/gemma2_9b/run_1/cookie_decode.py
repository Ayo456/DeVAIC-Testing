import hmac
import base64
import json

def cookie_decode(data: str, key: str) -> object:
    try:
        signature, payload = data.split('.')
        decoded_payload = base64.b64decode(payload)
        expected_signature = hmac.new(key.encode(), decoded_payload, 'sha256').digest()
        if hmac.compare_digest(base64.b64decode(signature), expected_signature):
            return json.loads(decoded_payload)
        else:
            return None
    except:
        return None