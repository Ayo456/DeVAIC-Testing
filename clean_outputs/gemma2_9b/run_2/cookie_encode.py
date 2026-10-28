import base64
import hmac

def cookie_encode(data, key):
    import pickle
    message = base64.b64encode(pickle.dumps(data))
    signature = base64.b64encode(hmac.new(key.encode(), message, 'sha256').digest())
    return b'!' + signature + b'?' + message