```python
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
                    user, password = b64decode(auth_header[6:]).decode('utf-8').split(':', 1)
                    if check_func(user, password):
                        return f(*args, **kwargs)
                except Exception:
                    pass
            return Response('Unauthorized', 401, {'WWW-Authenticate': 'Basic realm="Login Required"'})
        return decorated
    return decorator
```