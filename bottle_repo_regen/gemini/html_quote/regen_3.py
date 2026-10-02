# regen 3
import html


def html_quote(string: str) -> str:
    if not string:
        return '""'
    return f'"{html.escape(string, quote=True)}"'
