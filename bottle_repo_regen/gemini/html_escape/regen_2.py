# regen 2
import html


def html_escape(string: str) -> str:
    """Escape special HTML characters (&, <, >, ", ') into their corresponding entity codes."""
    if not isinstance(string, str):
        string = str(string)

    return html.escape(string, quote=True)
