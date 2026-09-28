# regen 1
from werkzeug.exceptions import HTTPException
from werkzeug.wrappers import Response


class RedirectException(HTTPException):
    """Custom HTTP exception carrying a response to abort execution."""

    def __init__(self, response: Response):
        super().__init__(response=response)


def redirect(
    url: str,
    code: int = None,
    environ: dict = None,
    http_version: str = "HTTP/1.1",
):
    """Trigger an HTTP redirection by raising an exception carrying the response.

    Defaults to status 303 for HTTP/1.1+ and 302 for older protocols (HTTP/1.0).
    """
    if code is None:
        if environ is not None:
            http_version = environ.get("SERVER_PROTOCOL", http_version)

        version_str = http_version.upper().replace("HTTP/", "")
        try:
            is_http_11_or_higher = float(version_str) >= 1.1
        except ValueError:
            is_http_11_or_higher = True

        code = 303 if is_http_11_or_higher else 302

    response = Response(
        response=f'Redirecting to <a href="{url}">{url}</a>',
        status=code,
        headers={"Location": url},
        mimetype="text/html",
    )

    raise RedirectException(response)

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