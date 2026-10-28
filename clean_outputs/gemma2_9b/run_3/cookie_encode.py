def cookie_encode(data, key):
    import base64
    import hmac
    from json import dumps
    message = base64.b64encode(dumps(data).encode())
    signature = base64.b64encode(hmac.new(key.encode(), message, 'sha256').digest())
    return b'!' + signature + b'?' + message