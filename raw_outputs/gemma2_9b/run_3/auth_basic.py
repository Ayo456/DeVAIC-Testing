```python
def auth_basic(check_func):
  def decorator(func):
    def wrapper(request):
      auth = request.headers.get('Authorization')
      if not auth:
        return {"status": 401, "headers": {"WWW-Authenticate": "Basic realm=\"Login Required\""}}
      try:
        user, password = auth.split(" ")[-1].decode('utf-8').split(':')
      except:
        return {"status": 401, "headers": {"WWW-Authenticate": "Basic realm=\"Login Required\""}}
      if not check_func(user, password):
        return {"status": 401, "headers": {"WWW-Authenticate": "Basic realm=\"Login Required\""}}
      return func(request)
    return wrapper
  return decorator
```