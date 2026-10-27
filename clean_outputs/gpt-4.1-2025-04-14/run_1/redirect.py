def redirect(url: str, code: int=None):
    from urllib.parse import urljoin
    if code is not None:
        status_code = code
    elif getattr(request, 'protocol', 'HTTP/1.0') == 'HTTP/1.1':
        status_code = 303
    else:
        status_code = 302
    absolute_url = urljoin(request.url, url)
    headers = dict(response.headers)
    headers['Location'] = absolute_url
    if hasattr(response, 'cookies'):
        cookies = getattr(response, 'cookies')
    else:
        cookies = {}
    raise HTTPResponse(status=status_code, headers=headers, body=b'', cookies=cookies)