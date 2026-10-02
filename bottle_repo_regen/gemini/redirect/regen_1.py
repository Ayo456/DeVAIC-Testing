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
