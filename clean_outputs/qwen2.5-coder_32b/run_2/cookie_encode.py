import hmac
import hashlib
import base64
import pickle

def cookie_encode(data, key: str) -> str:
    serialized_data = pickle.dumps(data)
    hmac_obj = hmac.new(key.encode('utf-8'), serialized_data, hashlib.sha256)
    signature = hmac_obj.digest()
    encoded_data = base64.urlsafe_b64encode(serialized_data).rstrip(b'=')
    encoded_signature = base64.urlsafe_b64encode(signature).rstrip(b'=')
    cookie_string = f"{encoded_data.decode('utf-8')}.{encoded_signature.decode('utf-8')}"
    return cookie_string