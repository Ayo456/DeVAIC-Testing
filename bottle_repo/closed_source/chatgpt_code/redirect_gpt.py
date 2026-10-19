class HTTPResponseException(Exception):
    def __init__(self, status, headers=None, body=""):
        self.status = status
        self.headers = headers or {}
        self.body = body
        super().__init__(body)


def redirect(url: str, code: int = None):
    import os

    if code is None:
        protocol = os.environ.get("SERVER_PROTOCOL", "HTTP/1.1")
        code = 303 if protocol == "HTTP/1.1" else 302

    raise HTTPResponseException(
        status=code,
        headers={"Location": url}
    )