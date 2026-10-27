```python
def auth_basic(check, realm="private", text="Access denied"):
    def decorator(handler):
        def wrapped(*args, **kwargs):
            credentials = request.auth
            if not credentials or not check(*credentials):
                response = HTTPError(401, text)
                response.add_header('WWW-Authenticate', f'Basic realm="{realm}"')
                return response
            return handler(*args, **kwargs)
        return wrapped
    return decorator
```