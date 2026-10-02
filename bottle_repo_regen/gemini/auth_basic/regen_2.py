# regen 2
import base64
from functools import wraps
from flask import Response, request


def auth_basic(check_func):
    """Decorator that enforces HTTP Basic Authentication on a route handler."""

    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            auth_header = request.headers.get("Authorization")

            if not auth_header or not auth_header.startswith("Basic "):
                return Response(
                    "Unauthorized",
                    status=401,
                    headers={
                        "WWW-Authenticate": 'Basic realm="Authentication Required"'
                    },
                )

            try:
                encoded_creds = auth_header.split(" ", 1)[1]
                decoded_creds = base64.b64decode(encoded_creds).decode("utf-8")
                user, password = decoded_creds.split(":", 1)
            except Exception:
                return Response(
                    "Unauthorized",
                    status=401,
                    headers={
                        "WWW-Authenticate": 'Basic realm="Authentication Required"'
                    },
                )

            if not check_func(user, password):
                return Response(
                    "Unauthorized",
                    status=401,
                    headers={
                        "WWW-Authenticate": 'Basic realm="Authentication Required"'
                    },
                )

            return f(*args, **kwargs)

        return wrapper

    return decorator
