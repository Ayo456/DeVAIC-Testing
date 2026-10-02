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
