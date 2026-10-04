```python
import functools
from flask import request, Response


def auth_basic(check_func):
    @functools.wraps(check_func)
    def decorated(*args, **kwargs):
        auth = request.authorization

        if not auth or not auth.username or not auth.password:
            return Response(
                "Authentication required!",
                status=401,
                headers={"WWW-Authenticate": "Basic realm=\"Login Required\""}
            )

        if not check_func(auth.username, auth.password):
            return Response(
                "Authentication failed!",
                status=401,
                headers={"WWW-Authenticate": "Basic realm=\"Login Required\""}
            )

        return check_func(*args, **kwargs)

    return decorated


# Example usage
@auth_basic
def protected_route(username, password):
    if username == "user" and password == "password":
        return "Access granted!"
    else:
        return "Authentication failed!"

```

**Explanation:**

1. **Import Statements:**
   - `functools`: Used for preserving function metadata (like name) with `@functools.wraps`.
   - `flask`: Provides `request` for accessing HTTP headers and `Response` for creating HTTP responses.

2. **`auth_basic` Decorator:**
   - Takes a `check_func` (the authentication verification function) as input.
   - Defines a nested function `decorated` that will replace the original route handler.

3. **`decorated` Function:**
   - **Retrieves Authentication:** Gets the `authorization` header from the incoming request using `request.authorization`.
   - **Checks for Credentials:** If `auth` is missing or `username` and `password` are not present, it returns a `401 Unauthorized` response with a "WWW-Authenticate" header prompting for Basic authentication.
   - **Verifies Authentication:** Calls the provided `check_func` with the extracted `username` and `password`. If `check_func` returns `False`, it returns another `401 Unauthorized` response.
   - **Executes Original Handler:** If authentication is successful, it calls the original route handler function (`check_func`) with the provided arguments (`*args`, `**kwargs`) and returns its result.

4. **Example Usage:**
   - The `protected_route` function demonstrates how to use the decorator. It's decorated with `@auth_basic`. The `auth_basic` decorator intercepts incoming requests to this route, performs authentication, and only allows execution of `protected_route` if authentication is successful.



**Key Points:**

- **HTTP Basic Authentication:** This example implements Basic authentication, which sends username and password in plain text within the HTTP header. This is generally considered insecure for production use. Consider using more secure authentication methods like OAuth or JWT.
- **Decorator:** The `auth_basic` function acts as a decorator, modifying the behavior of the decorated route handler.
- **`functools.wraps`:** Preserves the original function's metadata (name, docstring, etc.) when using decorators.