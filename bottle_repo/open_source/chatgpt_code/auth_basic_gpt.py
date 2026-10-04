import base64
from functools import wraps


def auth_basic(check_func):
    def decorator(handler):
        @wraps(handler)
        def wrapper(request, *args, **kwargs):
            header = request.headers.get("Authorization")

            if header and header.startswith("Basic "):
                try:
                    encoded = header.split(" ", 1)[1]
                    decoded = base64.b64decode(encoded, validate=True).decode("utf-8")
                    user, password = decoded.split(":", 1)

                    if check_func(user, password):
                        return handler(request, *args, **kwargs)
                except (ValueError, UnicodeDecodeError):
                    pass

            return (
                "Unauthorized",
                401,
                {"WWW-Authenticate": 'Basic realm="Authentication Required"'}
            )

        return wrapper

    return decorator