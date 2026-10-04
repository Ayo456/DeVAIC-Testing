import base64

def parse_auth(header: str) -> tuple:
    if not isinstance(header, str):
        return None
    parts = header.split(' ', 1)
    if len(parts) != 2:
        return None
    scheme, parameter = parts
    if scheme.lower() == 'basic':
        try:
            decoded = base64.b64decode(parameter).decode('utf-8')
            user, password = decoded.split(':', 1)
            return (user, password)
        except (base64.binascii.Error, ValueError):
            return None
    else:
        return (scheme, parameter)