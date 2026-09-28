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

# regen 3
import base64
from functools import wraps
from flask import request, Response


def auth_basic(check_func):
    """
    Decorator for route handlers enforcing HTTP Basic Authentication.
    """
    def unauthorized_response():
        return Response(
            "Unauthorized Access",
            status=401,
            headers={"WWW-Authenticate": 'Basic realm="Authentication Required"'}
        )

    def decorator(route_handler):
        @wraps(route_handler)
        def wrapper(*args, **kwargs):
            auth_header = request.headers.get("Authorization")
            if not auth_header or not auth_header.startswith("Basic "):
                return unauthorized_response()

            try:
                encoded_creds = auth_header.split(" ", 1)[1].strip()
                decoded_creds = base64.b64decode(encoded_creds).decode("utf-8")
                username, password = decoded_creds.split(":", 1)
            except Exception:
                return unauthorized_response()

            if not check_func(username, password):
                return unauthorized_response()

            return route_handler(*args, **kwargs)

        return wrapper

    return decorator