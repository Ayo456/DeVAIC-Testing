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

# regen 2
import base64
from functools import wraps

def auth_basic(check_func):
    def decorator(handler):
        @wraps(handler)
        def wrapper(*args, **kwargs):
            auth = request.headers.get("Authorization")

            if auth:
                try:
                    method, encoded = auth.split(None, 1)

                    if method.lower() == "basic":
                        decoded = base64.b64decode(encoded).decode("utf-8")
                        user, password = decoded.split(":", 1)

                        if check_func(user, password):
                            return handler(*args, **kwargs)
                except (ValueError, UnicodeDecodeError):
                    pass

            return HTTPResponse(
                status=401,
                body="Unauthorized",
                headers={"WWW-Authenticate": 'Basic realm="Restricted"'}
            )

        return wrapper

    return decorator

# regen 3
import base64
from functools import wraps
from bottle import request, HTTPResponse

def auth_basic(check_func):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            auth = request.headers.get("Authorization")

            if not auth or not auth.startswith("Basic "):
                return HTTPResponse(
                    status=401,
                    body="Unauthorized",
                    headers={"WWW-Authenticate": 'Basic realm="private"'}
                )

            try:
                encoded = auth.split(" ", 1)[1]
                decoded = base64.b64decode(encoded).decode("utf-8")
                user, password = decoded.split(":", 1)
            except (ValueError, UnicodeDecodeError):
                return HTTPResponse(
                    status=401,
                    body="Unauthorized",
                    headers={"WWW-Authenticate": 'Basic realm="private"'}
                )

            if not check_func(user, password):
                return HTTPResponse(
                    status=401,
                    body="Unauthorized",
                    headers={"WWW-Authenticate": 'Basic realm="private"'}
                )

            return func(*args, **kwargs)

        return wrapper
    return decorator