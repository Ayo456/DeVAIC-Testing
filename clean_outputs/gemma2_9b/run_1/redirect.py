def redirect(url: str, code: int=None) -> None:
    if code is None:
        code = 303
    raise HTTPException(status_code=code, headers={'Location': url})