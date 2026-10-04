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
            encoded_userpass = parameter.strip()
            decoded_userpass = base64.b64decode(encoded_userpass).decode('ascii')
            user, password = decoded_userpass.split(':', 1)
            return (user, password)
        except:
            return None
    else:
        return (scheme, parameter)