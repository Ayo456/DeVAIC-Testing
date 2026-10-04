from functools import wraps
from flask import request, Response

def auth_basic(check_func):

    def decorator(f):

        @wraps(f)
        def decorated(*args, **kwargs):
            auth_header = request.headers.get('Authorization')
            if not auth_header:
                return Response('Could not verify your access level for that URL.\nYou have to login with proper credentials', 401, {'WWW-Authenticate': 'Basic realm="Login Required"'})
            if not auth_header.startswith('Basic '):
                return Response('Invalid Authorization header format', 401, {'WWW-Authenticate': 'Basic realm="Login Required"'})
            import base64
            credentials = auth_header.split(' ')[1]
            try:
                decoded_credentials = base64.b64decode(credentials).decode('utf-8')
                user, password = decoded_credentials.split(':', 1)
            except (base64.binascii.Error, ValueError):
                return Response('Invalid Authorization header format', 401, {'WWW-Authenticate': 'Basic realm="Login Required"'})
            if not check_func(user, password):
                return Response('Could not verify your access level for that URL.\nYou have to login with proper credentials', 401, {'WWW-Authenticate': 'Basic realm="Login Required"'})
            return f(*args, **kwargs)
        return decorated
    return decorator

def check_credentials(user, password):
    return user == 'admin' and password == 'secret'

@app.route('/protected')
@auth_basic(check_credentials)
def protected_route():
    return 'This is a protected route.'