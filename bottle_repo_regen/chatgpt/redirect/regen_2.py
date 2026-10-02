# regen 2
def redirect(url: str, code: int = None):
    if code is None:
        code = 303 if request.environ.get("SERVER_PROTOCOL") == "HTTP/1.1" else 302

    res = response.copy(cls=HTTPResponse)
    res.status = code
    res.body = ""
    res.set_header("Location", urljoin(request.url, url))

    raise res
