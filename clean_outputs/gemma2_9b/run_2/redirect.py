import http.server

def redirect(url: str, code: int=None) -> None:
    if code is None:
        code = 303
    response = http.server.BaseHTTPRequestHandler.make_response(code)
    response.send_header('Location', url)
    raise http.server.HTTPServer.HTTPException(response)