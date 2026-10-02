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
