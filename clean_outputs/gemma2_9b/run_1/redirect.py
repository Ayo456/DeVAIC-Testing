from http.server import HTTPResponse

def redirect(url: str, code: int=None) -> None:
    if code is None:
        code = 303 if request.method == 'GET' else 302
    response = HTTPResponse(url, status=code, headers={'Location': url})
    raise response