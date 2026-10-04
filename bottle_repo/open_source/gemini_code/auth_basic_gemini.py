import base64
from functools import wraps

def auth_basic(check_func):
    def decorator(handler):
        @wraps(handler)
        def wrapper(*args, **kwargs):
            header = None
            if "request" in kwargs:
                req = kwargs["request"]
                header = getattr(req, "headers", {}).get("Authorization") or getattr(req, "environ", {}).get("HTTP_AUTHORIZATION")
            elif args:
                req = args[0]
                if hasattr(req, "headers"):
                    header = req.headers.get("Authorization")
                elif hasattr(req, "environ"):
                    header = req.environ.get("HTTP_AUTHORIZATION")
                elif isinstance(req, dict):
                    header = req.get("HTTP_AUTHORIZATION") or req.get("Authorization")

            def unauthorized():
                body = b"Unauthorized"
                headers = [
                    ("Content-Type", "text/plain; charset=utf-8"),
                    ("WWW-Authenticate", 'Basic realm="Login Required"')
                ]
                return 401, headers, body

            if not header or not isinstance(header, str):
                return unauthorized()

            parts = header.strip().split(None, 1)
            if len(parts) != 2 or parts[0].lower() != "basic":
                return unauthorized()

            try:
                decoded = base64.b64decode(parts[1].strip()).decode("utf-8")
                if ":" not in decoded:
                    return unauthorized()
                username, password = decoded.split(":", 1)
            except Exception:
                return unauthorized()

            if not check_func(username, password):
                return unauthorized()

            return handler(*args, **kwargs)
        return wrapper
    return decorator