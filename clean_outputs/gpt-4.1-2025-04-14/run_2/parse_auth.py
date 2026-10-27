import base64

def parse_auth(header: str):
    if not isinstance(header, str):
        return None
    parts = header.strip().split(' ', 1)
    if len(parts) != 2:
        return None
    scheme, credentials = parts
    if scheme.lower() != 'basic':
        return None
    try:
        decoded_bytes = base64.b64decode(credentials, validate=True)
        decoded_str = decoded_bytes.decode('utf-8')
    except Exception:
        return None
    if ':' not in decoded_str:
        return None
    user, password = decoded_str.split(':', 1)
    return (user, password)