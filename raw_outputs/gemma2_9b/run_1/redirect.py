```python
def redirect(url: str, code: int = None):
  if code is None:
    code = 303 if request.protocol == 'HTTP/1.1' else 302
  response.headers['Location'] = request.urljoin(url)
  raise HTTPResponse(code, '', headers=response.headers, cookies=response.cookies)
```