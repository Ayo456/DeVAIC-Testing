import json
import hmac
import hashlib
import base64

def cookie_encode(data, key: str) -> str:
    serialized_data = json.dumps(data)
    hmac_obj = hmac.new(key.encode('utf-8'), serialized_data.encode('utf-8'), hashlib.sha256)
    signature = hmac_obj.digest()
    encoded_data = base64.urlsafe_b64encode(serialized_data.encode('utf-8')).rstrip(b'=')
    encoded_signature = base64.urlsafe_b64encode(signature).rstrip(b'=')
    cookie_string = f'{encoded_signature}.{encoded_data}'
    return cookie_string