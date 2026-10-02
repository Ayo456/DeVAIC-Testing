# regen 3
import html

def html_escape(string: str) -> str:
    return html.escape(str(string), quote=True)
