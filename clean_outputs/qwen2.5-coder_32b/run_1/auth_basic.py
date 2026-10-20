from functools import wraps
from base64 import b64decode
from flask import request, Response

def auth_basic(check_func):

    def decorator(f):

        @wraps(f)
        def decorated(*args, **kwargs):
            auth_header = request.headers.get('Authorization')
            if auth_header and auth_header.startswith('Basic '):
                try:
                    encoded_credentials = auth_header.split(' ')[1]
                    decoded_credentials = b64decode(encoded_credentials).decode('utf-8')
                    user, password = decoded_credentials.split(':', 1)
                    if check_func(user, password):
                        return f(*args, **kwargs)
                except Exception:
                    pass
            return Response('Unauthorized', 401, {'WWW-Authenticate': 'Basic realm="Login Required"'})
        return decorated
    return decorator