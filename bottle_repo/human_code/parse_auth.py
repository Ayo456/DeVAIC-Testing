def parse_auth(header):
    try:
        method, data = header.split(None, 1)
        if method.lower() == 'basic':
            user, pwd = touni(base64.b64decode(tob(data))).split(':',1)
            return user, pwd
    except (KeyError, ValueError):
        return None