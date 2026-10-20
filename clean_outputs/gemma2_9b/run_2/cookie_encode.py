import hmac
import base64
from urllib.parse import quote

def cookie_encode(data, key: str) -> str:
    payload = base64.urlsafe_b64encode(serialize(data)).decode()
    signature = hmac.new(key.encode(), payload.encode(), 'sha256').digest()
    return f'hmac={quote(base64.urlsafe_b64encode(signature).decode())}; payload={quote(payload)}'

def serialize(data):
    return str(data).encode()