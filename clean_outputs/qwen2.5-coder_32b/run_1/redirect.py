from werkzeug.exceptions import HTTPException

class Redirect(HTTPException):

    def __init__(self, url: str, code: int=None):
        self.code = code if code is not None else 303
        self.headers = {'Location': url}

def redirect(url: str, code: int=None):
    raise Redirect(url, code)