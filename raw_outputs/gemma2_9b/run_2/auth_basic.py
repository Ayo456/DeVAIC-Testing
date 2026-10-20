```python
def auth_basic(check_func):
  def decorator(handler):
    def inner(request):
      auth = request.headers.get('Authorization')
      if auth:
        try:
          user, password = auth.split(' ')[1].decode('base64').split(':')
          if check_func(user, password):
            return handler(request)
          else:
            return 'HTTP/1.1 401 Unauthorized\r\nWWW-Authenticate: Basic realm="Restricted Area"\r\n'
        except:
          return 'HTTP/1.1 401 Unauthorized\r\nWWW-Authenticate: Basic realm="Restricted Area"\r\n'
      else:
        return 'HTTP/1.1 401 Unauthorized\r\nWWW-Authenticate: Basic realm="Restricted Area"\r\n'
    return inner
  return decorator
```