def redirect(url: str, code: int=None):
    from urllib.parse import urljoin
    absolute_url = urljoin(request.url, url)
    if code is None:
        code = 303 if request.protocol_version == 'HTTP/1.1' else 302
    response.headers['Location'] = absolute_url
    raise HTTPResponse(status=code, headers=response.headers, cookies=response.cookies)