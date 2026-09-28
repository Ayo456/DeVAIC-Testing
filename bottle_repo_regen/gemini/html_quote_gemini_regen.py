# regen 1
import html


def html_quote(string: str) -> str:
    if not string:
        return '""'
    escaped = html.escape(string, quote=True)
    return f'"{escaped}"'

# regen 2
import html


def html_quote(string: str) -> str:
    if not string:
        return '""'
    escaped = html.escape(string, quote=True)
    return f'"{escaped}"'

# regen 3
import html


def html_quote(string: str) -> str:
    if not string:
        return '""'
    return f'"{html.escape(string, quote=True)}"'