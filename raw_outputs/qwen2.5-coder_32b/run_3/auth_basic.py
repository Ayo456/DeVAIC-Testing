Certainly! Below is a Python function `auth_basic` that acts as a decorator for route handlers. This function extracts HTTP Basic authentication credentials from incoming HTTP headers, executes a provided `check_func(user, password)`, and returns an HTTP 401 Unauthorized response if the authentication fails or if credentials are missing.

This implementation assumes you are using a web framework like Flask. If you are using a different framework, the way to extract headers and return responses might differ slightly.

Here is the implementation:

```python
from functools import wraps
from flask import request, Response

def auth_basic(check_func):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            auth = request.authorization
            if not auth or not check_func(auth.username, auth.password):
                return Response(
                    'Could not verify your access level for that URL.\n'
                    'You have to login with proper credentials', 401,
                    {'WWW-Authenticate': 'Basic realm="Login Required"'})
            return f(*args, **kwargs)
        return decorated_function
    return decorator

# Example usage:
# @app.route('/protected')
# @auth_basic(check_credentials)
# def protected():
#     return "This is a protected route."

# Example check function:
# def check_credentials(username, password):
#     return username == 'admin' and password == 'secret'
```

### Explanation:

1. **Decorator Definition**:
   - `auth_basic(check_func)`: This is the main decorator function that takes another function `check_func` as an argument. This `check_func` is expected to take `user` and `password` as parameters and return `True` if the credentials are valid, `False` otherwise.

2. **Inner Decorator**:
   - `decorator(f)`: This function takes a function `f` (the route handler) and returns a wrapped version of it.

3. **Wrapped Function**:
   - `decorated_function(*args, **kwargs)`: This is the actual function that will be called when the route is accessed.
   - `request.authorization`: This extracts the authorization header from the request. If the header is present, it will be a dictionary-like object with `username` and `password` keys.
   - If `auth` is `None` (meaning no authorization header was provided) or `check_func(auth.username, auth.password)` returns `False` (meaning the credentials are invalid), a `401 Unauthorized` response is returned with the `WWW-Authenticate` header set to `Basic realm="Login Required"`.
   - If the credentials are valid, the original function `f` is called with its arguments.

4. **Usage**:
   - The `@auth_basic(check_credentials)` decorator is used to protect routes. The `check_credentials` function should be defined to check the validity of the provided credentials.

This implementation should work with Flask and can be adapted for other web frameworks by adjusting how headers are accessed and responses are returned.