import base64

def parse_auth(header: str):
    if not isinstance(header, str):
        return None
    parts = header.split(' ', 1)
    if len(parts) != 2:
        return None
    scheme, param = parts
    if scheme.lower() == 'basic':
        try:
            decoded = base64.b64decode(param).decode('utf-8')
            user, password = decoded.split(':', 1)
            return (user, password)
        except (base64.binascii.Error, UnicodeDecodeError, ValueError):
            return None
    return (scheme, param)