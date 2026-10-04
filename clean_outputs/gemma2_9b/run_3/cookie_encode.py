import hmac
import base64
import json
from urllib.parse import quote

def cookie_encode(data, key: str) -> str:
    payload = json.dumps(data)
    signature = hmac.new(key.encode(), payload.encode(), digestmod='sha256').digest()
    signature_b64 = base64.b64encode(signature).decode('ascii')
    signature_url = quote(signature_b64)
    cookie_string = f'hmac={signature_url}; path=/; HttpOnly'
    return cookie_string