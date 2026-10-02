# regen 1
from bottle import request, HTTPResponse
from urllib.parse import urljoin

def redirect(url: str, code: int = None):
    if code is None:
        code = 303 if request.environ.get("SERVER_PROTOCOL") == "HTTP/1.1" else 302

    response = HTTPResponse(status=code)
    response.set_header("Location", urljoin(request.url, url))
    raise response
