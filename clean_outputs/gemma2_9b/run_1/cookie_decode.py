import json
from hashlib import sha256

def cookie_decode(data: str, key: str) -> object:
    try:
        payload, signature = data.split('.')
        decoded_payload = json.loads(payload)
        calculated_signature = sha256(payload.encode()).hexdigest()
        if calculated_signature == signature:
            return decoded_payload
        else:
            return None
    except:
        return None