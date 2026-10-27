def redirect(url: str, code: int=None):
    from urllib.parse import urljoin
    protocol = getattr(request, 'protocol', 'HTTP/1.0')
    if code is None:
        status_code = 303 if protocol == 'HTTP/1.1' else 302
    else:
        status_code = code
    base_url = getattr(request, 'url', '/')
    absolute_url = urljoin(base_url, url)
    headers = dict(getattr(response, 'headers', {}))
    headers['Location'] = absolute_url
    cookies = getattr(response, 'cookies', {})
    raise HTTPResponse(status=status_code, headers=headers, body=b'', cookies=cookies)