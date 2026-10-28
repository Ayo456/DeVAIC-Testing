import html

def html_escape(string: str) -> str:
    if not isinstance(string, str):
        string = str(string)
    return html.escape(string, quote=True)