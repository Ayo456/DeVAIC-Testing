from functools import wraps
from flask import request, Response
import base64

def auth_basic(check_func):

    def decorator(f):

        @wraps(f)
        def decorated_function(*args, **kwargs):
            auth_header = request.headers.get('Authorization')
            if not auth_header or not auth_header.startswith('Basic '):
                return Response('Could not verify your access level for that URL.\nYou have to login with proper credentials', 401, {'WWW-Authenticate': 'Basic realm="Login Required"'})
            auth_decoded = base64.b64decode(auth_header.split(' ')[1]).decode('utf-8')
            username, password = auth_decoded.split(':', 1)
            if not check_func(username, password):
                return Response('Could not verify your access level for that URL.\nYou have to login with proper credentials', 401, {'WWW-Authenticate': 'Basic realm="Login Required"'})
            return f(*args, **kwargs)
        return decorated_function
    return decorator

def check_credentials(user, password):
    return user == 'admin' and password == 'secret'

@app.route('/protected')
@auth_basic(check_credentials)
def protected_route():
    return 'This is a protected route.'