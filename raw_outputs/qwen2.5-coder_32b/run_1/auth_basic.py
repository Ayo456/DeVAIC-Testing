Certainly! Below is a Python function named `auth_basic` that acts as a decorator for route handlers. It extracts HTTP Basic authentication credentials from incoming HTTP headers, executes `check_func(user, password)`, and returns an HTTP 401 Unauthorized response with the proper authentication challenge header if authentication fails or credentials are missing.

This example assumes you are using a web framework like Flask. If you are using a different framework, the response creation part might need to be adjusted accordingly.

```python
from functools import wraps
from flask import request, Response
import base64

def auth_basic(check_func):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            # Extract the Authorization header
            auth_header = request.headers.get('Authorization')
            
            if not auth_header or not auth_header.startswith('Basic '):
                # Return 401 Unauthorized if no or invalid Authorization header
                return Response(
                    'Could not verify your access level for that URL.\n'
                    'You have to login with proper credentials', 401,
                    {'WWW-Authenticate': 'Basic realm="Login Required"'})
            
            # Decode the base64 encoded credentials
            auth_decoded = base64.b64decode(auth_header.split(' ')[1]).decode('utf-8')
            username, password = auth_decoded.split(':', 1)
            
            # Check the credentials using the provided check_func
            if not check_func(username, password):
                # Return 401 Unauthorized if credentials are invalid
                return Response(
                    'Could not verify your access level for that URL.\n'
                    'You have to login with proper credentials', 401,
                    {'WWW-Authenticate': 'Basic realm="Login Required"'})
            
            # If authentication is successful, proceed with the original function
            return f(*args, **kwargs)
        return decorated_function
    return decorator

# Example usage with a simple check function
def check_credentials(user, password):
    return user == 'admin' and password == 'secret'

@app.route('/protected')
@auth_basic(check_credentials)
def protected_route():
    return "This is a protected route."
```

### Explanation:
1. **Decorator Function**: The `auth_basic` function takes `check_func` as an argument and returns a decorator.
2. **Header Extraction**: It extracts the `Authorization` header from the request.
3. **Header Validation**: It checks if the header exists and starts with `Basic `.
4. **Decoding Credentials**: It decodes the base64-encoded credentials and splits them into `username` and `password`.
5. **Credential Validation**: It calls `check_func` with the extracted `username` and `password`.
6. **Response Handling**: If the credentials are invalid or missing, it returns a 401 Unauthorized response with the `WWW-Authenticate` header. Otherwise, it proceeds with the original function.

This decorator can be used to protect any route in your Flask application by simply adding `@auth_basic(check_func)` above the route handler function.