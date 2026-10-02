# regen 3
import html

def html_quote(string: str) -> str:
    if string is None or string == "":
        return '""'

    escaped = html.escape(string, quote=True)
    return f'"{escaped}"'
