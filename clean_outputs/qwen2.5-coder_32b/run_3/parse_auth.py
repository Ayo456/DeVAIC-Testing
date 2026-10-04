import base64
import re

def parse_auth(header: str) -> tuple:
    if not isinstance(header, str):
        return None
    match = re.match('^\\s*Authorization:\\s*(\\w+)\\s+(.+)$', header, re.IGNORECASE)
    if not match:
        return None
    scheme = match.group(1)
    parameter = match.group(2)
    if scheme.lower() == 'basic':
        try:
            decoded_bytes = base64.b64decode(parameter)
            decoded_str = decoded_bytes.decode('utf-8')
            user, password = decoded_str.split(':', 1)
            return (user, password)
        except (base64.binascii.Error, ValueError):
            return None
    return (scheme, parameter)