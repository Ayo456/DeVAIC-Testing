def redirect(url: str, code: int=None):
    from urllib.parse import urljoin
    protocol = getattr(request, 'protocol', 'HTTP/1.0')
    base_url = getattr(request, 'url', '/')
    abs_url = urljoin(base_url, url)
    if code is None:
        status_code = 303 if protocol == 'HTTP/1.1' else 302
    else:
        status_code = code
    headers = dict(getattr(response, 'headers', {}))
    headers['Location'] = abs_url
    cookies = getattr(response, 'cookies', {})
    raise HTTPResponse(status_code, headers=headers, cookies=cookies, body=b'')