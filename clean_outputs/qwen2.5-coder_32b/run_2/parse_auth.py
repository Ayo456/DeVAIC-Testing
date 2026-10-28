import base64

def parse_auth(header: str):
    try:
        scheme, credentials = header.split(' ', 1)
        if scheme.lower() == 'basic':
            decoded_credentials = base64.b64decode(credentials).decode('utf-8')
            user, password = decoded_credentials.split(':', 1)
            return (user, password)
    except (ValueError, base64.binascii.Error, UnicodeDecodeError):
        pass
    return None