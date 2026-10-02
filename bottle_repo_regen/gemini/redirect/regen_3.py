# regen 3
from werkzeug.exceptions import HTTPException
from werkzeug.wrappers import Response


class HTTPRedirectException(HTTPException):
    def __init__(self, response: Response):
        super().__init__(response=response)


def redirect(
    url: str, code: int = None, http_version: str = "HTTP/1.1"
) -> None:
    if code is None:
        code = 302 if http_version == "HTTP/1.0" else 303

    response = Response(
        status=code,
        headers={"Location": url},
    )

    raise HTTPRedirectException(response=response)
