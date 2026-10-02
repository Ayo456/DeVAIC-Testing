# regen 1
import functools
from bottle import request, HTTPError

def auth_basic(check_func):
    def decorator(route_func):
        @functools.wraps(route_func)
        def wrapper(*args, **kwargs):
            user, password = request.auth or (None, None)

            if user is None or not check_func(user, password):
                error = HTTPError(401, "Unauthorized")
                error.add_header(
                    "WWW-Authenticate",
                    'Basic realm="private"'
                )
                return error

            return route_func(*args, **kwargs)

        return wrapper

    return decorator
