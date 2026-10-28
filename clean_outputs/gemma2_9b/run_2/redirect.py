def redirect(url: str, code: int=None):
    if code is None:
        code = 303 if request.protocol == 'HTTP/1.1' else 302
    response.headers['Location'] = url
    response.headers.update(request.headers)
    response.cookies.update(request.cookies)
    raise HTTPResponse(status=code, body='', headers=response.headers)