import base64
import hashlib
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import padding
import json

def cookie_decode(data: str, key: str) -> object:
    try:
        decoded_data = base64.b64decode(data)
        payload_size = len(decoded_data) // 2
        payload = decoded_data[:payload_size]
        signature = decoded_data[payload_size:]
        private_key = serialization.load_pem_private_key(base64.b64decode(key), password=None, backend=default_backend())
        try:
            public_key = private_key.public_key()
            public_key.verify(signature, payload, padding.PSS(mgf=padding.MGF1(hashes.SHA256()), salt_length=padding.PSS.MAX_LENGTH), hashes.SHA256())
        except Exception as e:
            print(f'Signature verification failed: {e}')
            return None
        try:
            object = json.loads(payload.decode())
        except json.JSONDecodeError as e:
            print(f'Payload deserialization failed: {e}')
            return None
        return object
    except Exception as e:
        print(f'Cookie decoding failed: {e}')
        return None