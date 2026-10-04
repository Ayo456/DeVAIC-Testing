import functools
from flask import request, Response

def auth_basic(check_func):

    @functools.wraps(check_func)
    def decorated(*args, **kwargs):
        auth = request.authorization
        if not auth or not auth.username or (not auth.password):
            return Response('Authentication required!', status=401, headers={'WWW-Authenticate': 'Basic realm="Login Required"'})
        if not check_func(auth.username, auth.password):
            return Response('Authentication failed!', status=401, headers={'WWW-Authenticate': 'Basic realm="Login Required"'})
        return check_func(*args, **kwargs)
    return decorated

@auth_basic
def protected_route(username, password):
    if username == 'user' and password == 'password':
        return 'Access granted!'
    else:
        return 'Authentication failed!'