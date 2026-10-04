from functools import wraps
from flask import request, Response

def auth_basic(check_func):

    def decorator(f):

        @wraps(f)
        def decorated_function(*args, **kwargs):
            auth = request.authorization
            if not auth or not check_func(auth.username, auth.password):
                return Response('Could not verify your access level for that URL.\nYou have to login with proper credentials', 401, {'WWW-Authenticate': 'Basic realm="Login Required"'})
            return f(*args, **kwargs)
        return decorated_function
    return decorator