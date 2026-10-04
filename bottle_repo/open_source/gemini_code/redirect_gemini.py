from typing import Optional


class HTTPRedirect(Exception):
    def __init__(self, status: int, headers: dict[str, str]):
        self.status = status
        self.headers = headers
        super().__init__(f"Redirecting with status {status}")


def redirect(url: str, code: Optional[int] = None) -> None:
    if code is None:
        code = 303

    headers = {"Location": url}
    raise HTTPRedirect(code, headers)