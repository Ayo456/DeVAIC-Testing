# regen 1
import base64
from functools import wraps
from flask import Response, request


def auth_basic(check_func):
    """Decorator factory for HTTP Basic Authentication on route handlers."""

    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            auth_header = request.headers.get("Authorization")

            def unauthorized_response():
                return Response(
                    "Unauthorized",
                    status=401,
                    headers={"WWW-Authenticate": 'Basic realm="Login Required"'},
                )

            if not auth_header or not auth_header.startswith("Basic "):
                return unauthorized_response()

            try:
                encoded_creds = auth_header.split(" ", 1)[1].strip()
                decoded_creds = base64.b64decode(encoded_creds).decode("utf-8")
                user, password = decoded_creds.split(":", 1)
            except Exception:
                return unauthorized_response()

            if not check_func(user, password):
                return unauthorized_response()

            return f(*args, **kwargs)

        return wrapper

    return decorator
