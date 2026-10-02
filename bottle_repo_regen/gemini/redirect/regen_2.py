# regen 2
class HTTPException(Exception):
    """Exception raised to interrupt execution and send an HTTP response."""

    def __init__(self, response):
        super().__init__(response)
        self.response = response


class Response:
    def __init__(self, status_code: int, headers: dict = None, body: str = ""):
        self.status_code = status_code
        self.headers = headers or {}
        self.body = body


def redirect(url: str, code: int = None, http_version: str = "HTTP/1.1") -> None:
    if code is None:


        code = 303 if http_version >= "HTTP/1.1" else 302

    response = Response(status_code=code, headers={"Location": url})
    raise HTTPException(response)
