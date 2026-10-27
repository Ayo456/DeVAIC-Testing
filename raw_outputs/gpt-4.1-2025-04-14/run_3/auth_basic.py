```python
def auth_basic(check, realm="private", text="Access denied"):
    def decorator(func):
        def wrapper(*args, **kwargs):
            creds = getattr(request, 'auth', None)
            if not creds or not check(*creds):
                err = HTTPError(401, text)
                err.add_header('WWW-Authenticate', f'Basic realm="{realm}"')
                return err
            return func(*args, **kwargs)
        return wrapper
    return decorator
```