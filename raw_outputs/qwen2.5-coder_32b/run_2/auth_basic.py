Certainly! Below is a Python function named `auth_basic` that acts as a decorator for route handlers. This function will extract HTTP Basic authentication credentials from incoming HTTP headers, execute `check_func(user, password)`, and return an HTTP 401 Unauthorized response if authentication fails or credentials are missing.

For this implementation, I'll assume you're using a web framework like Flask. Here is how you can implement it:

```python
from functools import wraps
from flask import request, Response

def auth_basic(check_func):
    def decorator(f):
        @wraps(f)
        def decorated(*args, **kwargs):
            # Extract the Authorization header
            auth_header = request.headers.get('Authorization')
            
            if not auth_header:
                # If no Authorization header, return 401 with challenge
                return Response(
                    'Could not verify your access level for that URL.\n'
                    'You have to login with proper credentials', 401,
                    {'WWW-Authenticate': 'Basic realm="Login Required"'}
                )
            
            # Check if the header is a Basic Auth header
            if not auth_header.startswith('Basic '):
                return Response(
                    'Invalid Authorization header format', 401,
                    {'WWW-Authenticate': 'Basic realm="Login Required"'}
                )
            
            # Decode the base64 encoded credentials
            import base64
            credentials = auth_header.split(' ')[1]
            try:
                decoded_credentials = base64.b64decode(credentials).decode('utf-8')
                user, password = decoded_credentials.split(':', 1)
            except (base64.binascii.Error, ValueError):
                return Response(
                    'Invalid Authorization header format', 401,
                    {'WWW-Authenticate': 'Basic realm="Login Required"'}
                )
            
            # Call the provided check function
            if not check_func(user, password):
                return Response(
                    'Could not verify your access level for that URL.\n'
                    'You have to login with proper credentials', 401,
                    {'WWW-Authenticate': 'Basic realm="Login Required"'}
                )
            
            # If authentication is successful, call the original function
            return f(*args, **kwargs)
        return decorated
    return decorator

# Example usage with a simple check function
def check_credentials(user, password):
    # Replace this with your actual authentication logic
    return user == 'admin' and password == 'secret'

@app.route('/protected')
@auth_basic(check_credentials)
def protected_route():
    return "This is a protected route."
```

### Explanation:
1. **Decorator Definition**: The `auth_basic` function is a decorator factory that takes a `check_func` as an argument.
2. **Authorization Header Extraction**: The `Authorization` header is extracted from the request headers.
3. **Header Validation**: The function checks if the header is present and starts with `Basic `. If not, it returns a 401 Unauthorized response with the appropriate `WWW-Authenticate` header.
4. **Base64 Decoding**: The base64-encoded credentials are decoded, and the username and password are split.
5. **Authentication Check**: The `check_func` is called with the decoded username and password. If it returns `False`, a 401 Unauthorized response is returned.
6. **Route Execution**: If authentication is successful, the original route handler function is called.

This implementation can be adapted to other web frameworks with minor modifications, especially in how the request and response objects are handled.